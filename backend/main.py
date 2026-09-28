import logging
import asyncio
import random
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.models import LogEntry
from backend.tailer import tail_log_file
from backend.websocket_manager import manager
from backend.services.detector_adapter import DetectorAdapter
from backend.services.alert_publisher import AlertPublisher
from backend.simulator import write_log, NORMAL_LOGS, ANOMALY_PAYMENT_LOGS, ANOMALY_DB_LOGS, RECOVERY_LOGS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

detector = DetectorAdapter()
publisher = AlertPublisher()

async def process_log_entry(entry: LogEntry):
    try:
        result = detector.process_log(entry)
        await manager.broadcast(result.model_dump())
        await publisher.publish(result)
    except Exception as e:
        logger.error(f"Detector processing failed: {e}")

monitoring_task = None
traffic_gen_task = None
traffic_gen_state = {
    "running": False,
    "mode": "idle",
    "speed": 0.8,
    "logs_generated": 0
}

# Live Microservice State
shop_state = {
    "outage_mode": False,
    "failure_type": "stripe_timeout"
}

async def traffic_generator_loop():
    logger.info("Traffic generator background loop started")
    try:
        while traffic_gen_state["running"]:
            mode = traffic_gen_state["mode"]
            if mode == "normal":
                level, msg = random.choices(
                    NORMAL_LOGS,
                    weights=[30, 25, 20, 10, 10, 10, 5]
                )[0]
            elif mode in ("anomaly", "payment_outage"):
                level, msg = random.choice(ANOMALY_PAYMENT_LOGS)
            elif mode == "db_crash":
                level, msg = random.choice(ANOMALY_DB_LOGS)
            elif mode == "recovery":
                level, msg = random.choice(RECOVERY_LOGS)
            else:
                level, msg = ("INFO", "[traffic-gen] Heartbeat ping ok")

            # Write to app.log so file tailer naturally picks it up
            write_log(level, msg)
            traffic_gen_state["logs_generated"] += 1
            await asyncio.sleep(traffic_gen_state["speed"])
    except asyncio.CancelledError:
        logger.info("Traffic generator loop stopped")
    finally:
        traffic_gen_state["running"] = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Backend starting")
    global monitoring_task
    monitoring_task = asyncio.create_task(tail_log_file(process_log_entry))
    yield
    # Shutdown
    if monitoring_task:
        monitoring_task.cancel()
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass
    global traffic_gen_task
    if traffic_gen_task:
        traffic_gen_task.cancel()
    logger.info("Backend stopped")

app = FastAPI(
    title="Log Sentinel - Real-Time Anomaly Engine",
    description="Real-Time Log Ingestion, Statistical Anomaly Detection & AWS Alert System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health & System ──

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "log-anomaly-backend",
        "websocket_clients": len(manager.active_connections),
        "traffic_generator": traffic_gen_state
    }

# ── Universal Log Ingestion API (Kubernetes / FluentBit / OpenTelemetry) ──

class IngestLogPayload(BaseModel):
    timestamp: Optional[str] = None
    level: str = "INFO"
    message: str
    service: Optional[str] = "api-service"

@app.post("/api/v1/logs")
async def ingest_log(payload: IngestLogPayload):
    """Universal log ingestion endpoint. Accepts logs from any external service."""
    ts = payload.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{payload.service}] {payload.message}" if payload.service and not payload.message.startswith("[") else payload.message
    
    # Write to log file and process
    write_log(payload.level.upper(), formatted_msg)
    return {"status": "accepted", "timestamp": ts, "level": payload.level.upper()}

# ── Interactive Chaos / Traffic Control API ──

@app.post("/api/simulator/start")
async def start_simulator(
    mode: str = Query("normal", enum=["normal", "anomaly", "payment_outage", "db_crash", "recovery"]),
    speed: float = Query(0.8, ge=0.05, le=5.0)
):
    """Start automated live traffic generation (normal, payment outage, db crash, recovery)."""
    global traffic_gen_task
    if traffic_gen_task and not traffic_gen_task.done():
        traffic_gen_task.cancel()
    
    traffic_gen_state["running"] = True
    traffic_gen_state["mode"] = mode
    traffic_gen_state["speed"] = speed
    traffic_gen_task = asyncio.create_task(traffic_generator_loop())
    
    return {
        "status": "started",
        "mode": mode,
        "speed_seconds": speed
    }

@app.post("/api/simulator/stop")
async def stop_simulator():
    """Stop automated live traffic generation."""
    global traffic_gen_task
    if traffic_gen_task and not traffic_gen_task.done():
        traffic_gen_task.cancel()
    traffic_gen_state["running"] = False
    traffic_gen_state["mode"] = "stopped"
    return {"status": "stopped"}

@app.get("/api/simulator/status")
async def simulator_status():
    """Get current traffic generator status."""
    return traffic_gen_state

# ── Live E-Commerce Microservice Endpoints (Interactive Demo Target) ──

@app.get("/api/shop/products")
async def get_products():
    write_log("INFO", "[catalog-api] 24 products fetched (200 OK)")
    return [
        {"id": 1, "name": "Enterprise Cloud Server", "price": 299.99},
        {"id": 2, "name": "AI Observability Agent", "price": 49.99},
        {"id": 3, "name": "Log Stream Accelerator", "price": 119.00}
    ]

@app.post("/api/shop/checkout")
async def checkout_cart(cart_id: str = "cart_9841", amount: float = 149.99):
    """Simulates real checkout. Fails with 504 when outage is active."""
    if shop_state["outage_mode"]:
        write_log("ERROR", f"[payment-gateway] Stripe charge failed for cart={cart_id} ($ {amount:.2f}): HTTP 504 Gateway Timeout")
        raise HTTPException(status_code=504, detail="Payment Gateway Timeout - Bank API unreachable")
    
    write_log("INFO", f"[checkout-service] Payment authorized for cart={cart_id} ($ {amount:.2f}) - 200 OK")
    return {"status": "success", "order_id": f"ord_{random.randint(10000, 99999)}", "amount": amount}

@app.post("/api/shop/chaos/toggle-outage")
async def toggle_shop_outage(enable: Optional[bool] = None):
    if enable is None:
        shop_state["outage_mode"] = not shop_state["outage_mode"]
    else:
        shop_state["outage_mode"] = enable
    status_str = "ACTIVE (504 Outage)" if shop_state["outage_mode"] else "OFF (Healthy 200 OK)"
    write_log("WARNING" if shop_state["outage_mode"] else "INFO", f"[chaos-engine] Payment Gateway Outage toggled to: {status_str}")
    return {"outage_mode": shop_state["outage_mode"], "status": status_str}

# ── WebSocket Stream ──

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


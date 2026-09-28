import logging
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.tailer import tail_log_file
from backend.websocket_manager import manager
from backend.services.detector_adapter import DetectorAdapter
from backend.services.alert_publisher import AlertPublisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

detector = DetectorAdapter()
publisher = AlertPublisher()

async def process_log_entry(entry):
    try:
        result = detector.process_log(entry)
        await manager.broadcast(result.model_dump())
        await publisher.publish(result)
    except Exception as e:
        logger.error(f"Detector processing failed: {e}")

monitoring_task = None

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
    logger.info("Backend stopped")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "log-anomaly-backend",
        "websocket_clients": len(manager.active_connections)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from client, but we must handle connection drops
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

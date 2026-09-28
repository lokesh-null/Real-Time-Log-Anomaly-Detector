"""
Real Standalone E-Commerce & Payment Gateway Microservice
Runs on Port 5001 as an independent web server.
Logs every real incoming HTTP request in real time to logs/app.log.
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

LOG_FILE = "logs/app.log"
os.makedirs("logs", exist_ok=True)

app = FastAPI(
    title="E-Commerce Microservice (Real Target Service)",
    description="Real web service producing actual HTTP server logs for Sentinel to monitor",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service Outage State
service_health = {
    "payment_gateway": "HEALTHY", # HEALTHY | OUTAGE (504)
    "database": "HEALTHY",        # HEALTHY | DEADLOCK (500)
    "auth_service": "HEALTHY",    # HEALTHY | RATE_LIMITED (429)
}

def log_real_event(level: str, message: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {level} {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{line}\n")
        f.flush()
    print(f"[{level}] {message}")

# Real HTTP Middleware: Logs every single incoming HTTP request & status code
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        status_code = response.status_code

        if status_code >= 500:
            level = "ERROR"
        elif status_code >= 400:
            level = "WARNING"
        else:
            level = "INFO"

        msg = f"[{request.url.path}] {request.method} - HTTP {status_code} ({duration_ms:.1f}ms) Client: {request.client.host}"
        log_real_event(level, msg)
        return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        log_real_event("CRITICAL", f"[{request.url.path}] Unhandled Exception: {str(e)} ({duration_ms:.1f}ms)")
        raise e

@app.get("/")
async def root():
    return {"status": "online", "service": "real-ecommerce-microservice", "port": 5001}

@app.get("/api/products")
async def get_products():
    return [
        {"id": 101, "name": "Cloud Observability Platform", "price": 499.00, "in_stock": True},
        {"id": 102, "name": "High-Throughput Log Pipeline", "price": 199.00, "in_stock": True},
        {"id": 103, "name": "Real-Time Anomaly Engine", "price": 899.00, "in_stock": True},
    ]

@app.post("/api/auth/login")
async def login(username: str = "admin"):
    if service_health["auth_service"] == "RATE_LIMITED":
        raise HTTPException(status_code=429, detail="Too Many Requests - Rate limit exceeded")
    return {"token": "jwt_token_valid_9941", "expires_in": 3600}

@app.post("/api/orders/checkout")
async def checkout(cart_id: str = "cart_1001", amount: float = 249.99):
    if service_health["database"] == "DEADLOCK":
        raise HTTPException(status_code=500, detail="Database Connection Pool Exhausted: Deadlock on table 'orders'")
    return {"order_id": f"ord_{int(time.time())}", "status": "CONFIRMED", "amount": amount}

@app.post("/api/payments/charge")
async def process_payment(order_id: str = "ord_5521", amount: float = 249.99):
    if service_health["payment_gateway"] == "OUTAGE":
        # Simulate real upstream Stripe/Bank timeout
        time.sleep(0.1)
        raise HTTPException(status_code=504, detail="Stripe API Gateway Timeout - Bank payment network unreachable")
    return {"transaction_id": f"txn_{int(time.time()*1000)}", "status": "SUCCEEDED", "amount": amount}

# ── Outage / Chaos Injection Endpoints ──

@app.post("/chaos/inject/payment-outage")
async def inject_payment_outage():
    service_health["payment_gateway"] = "OUTAGE"
    log_real_event("CRITICAL", "[CHAOS INJECTED] Payment Gateway Outage activated: /api/payments/charge will return 504")
    return {"payment_gateway": "OUTAGE"}

@app.post("/chaos/inject/db-deadlock")
async def inject_db_deadlock():
    service_health["database"] = "DEADLOCK"
    log_real_event("CRITICAL", "[CHAOS INJECTED] Database deadlock activated: /api/orders/checkout will return 500")
    return {"database": "DEADLOCK"}

@app.post("/chaos/recover")
async def recover_all():
    service_health["payment_gateway"] = "HEALTHY"
    service_health["database"] = "HEALTHY"
    service_health["auth_service"] = "HEALTHY"
    log_real_event("INFO", "[SYSTEM RECOVERY] All services restored to HEALTHY: 200 OK")
    return {"status": "ALL_SERVICES_HEALTHY"}

if __name__ == "__main__":
    print("Starting Real E-Commerce Microservice on http://127.0.0.1:5001 ...")
    uvicorn.run(app, host="127.0.0.1", port=5001, log_level="warning")

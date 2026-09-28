"""
Real Network Traffic Blaster (HTTP Client)
Sends real HTTP requests over TCP to the E-Commerce Microservice (http://127.0.0.1:5001).
"""

import argparse
import time
import random
import urllib.request
import urllib.error
import json

TARGET_BASE = "http://127.0.0.1:5001"

def send_request(path: str, method: str = "GET", payload: dict = None):
    url = f"{TARGET_BASE}{path}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    headers = {"Content-Type": "application/json"} if payload else {}
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 0, str(e)

def run_normal_traffic(delay=0.6):
    print("🚀 Sending REAL HTTP traffic (200 OK normal shopping flow)...")
    actions = [
        ("/api/products", "GET", None),
        ("/api/auth/login", "POST", {"username": "shopper_49"}),
        ("/api/orders/checkout", "POST", {"cart_id": "cart_882", "amount": 129.99}),
        ("/api/payments/charge", "POST", {"order_id": "ord_991", "amount": 129.99}),
    ]
    while True:
        path, method, body = random.choice(actions)
        status, resp = send_request(path, method, body)
        print(f"--> {method} {path} | HTTP {status}")
        time.sleep(delay)

def run_outage_traffic(delay=0.25):
    print("🚨 Triggering Payment Outage on Microservice and blasting payment requests...")
    # Inject outage
    send_request("/chaos/inject/payment-outage", "POST", {})
    
    while True:
        # Blast payment charge requests that will fail with 504
        status, resp = send_request("/api/payments/charge", "POST", {"order_id": "ord_fail", "amount": 499.00})
        print(f"--> POST /api/payments/charge | HTTP {status} (OUTAGE)")
        time.sleep(delay)

def run_recovery():
    print("🟢 Sending Recovery signal to Microservice...")
    send_request("/chaos/recover", "POST", {})
    # Send healthy traffic
    run_normal_traffic(0.5)

def main():
    parser = argparse.ArgumentParser(description="Real HTTP Traffic Generator")
    parser.add_argument("--mode", choices=["normal", "anomaly", "outage", "recovery"], required=True)
    parser.add_argument("--delay", type=float, default=None)
    args = parser.parse_args()

    try:
        if args.mode == "normal":
            run_normal_traffic(args.delay or 0.6)
        elif args.mode in ("anomaly", "outage"):
            run_outage_traffic(args.delay or 0.25)
        elif args.mode == "recovery":
            run_recovery()
    except KeyboardInterrupt:
        print("\nTraffic blaster stopped.")

if __name__ == "__main__":
    main()

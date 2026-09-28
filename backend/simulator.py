import argparse
import os
import random
import time
from datetime import datetime

LOG_FILE = "logs/app.log"

MICROSERVICES = [
    "payment-gateway",
    "order-service",
    "auth-service",
    "inventory-api",
    "checkout-service",
    "database-cluster",
]

NORMAL_LOGS = [
    ("INFO", "[order-service] Order #49281 placed successfully ($129.99)"),
    ("INFO", "[payment-gateway] Stripe payment intent authorization succeeded (txn_3M2k4x)"),
    ("INFO", "[auth-service] JWT token validated for user_id=9821 (latency: 12ms)"),
    ("INFO", "[inventory-api] Inventory reserved for SKU-8841-A (warehouse: us-east)"),
    ("INFO", "[checkout-service] Shopping cart #8839 checked out (items: 3)"),
    ("INFO", "[database-cluster] Read query executed on replica-2 (latency: 4ms)"),
    ("WARNING", "[inventory-api] Low stock threshold reached for SKU-2910-B (remaining: 3)"),
]

ANOMALY_PAYMENT_LOGS = [
    ("ERROR", "[payment-gateway] Stripe API connection timeout after 5000ms (HTTP 504 Gateway Timeout)"),
    ("ERROR", "[payment-gateway] Card authorization failed: Upstream bank network unreachable"),
    ("ERROR", "[checkout-service] Payment processing exception: RemoteServiceUnavailable"),
    ("CRITICAL", "[payment-gateway] Circuit breaker tripped: Stripe gateway failure rate > 65%"),
    ("ERROR", "[order-service] Rollback transaction for Order #49290 due to payment failure"),
]

ANOMALY_DB_LOGS = [
    ("ERROR", "[database-cluster] Connection pool exhausted: Max clients limit (1000) reached"),
    ("ERROR", "[auth-service] Database query timeout (10000ms): could not acquire session lock"),
    ("CRITICAL", "[database-cluster] PostgreSQL deadlock detected on table 'orders'"),
    ("ERROR", "[order-service] Transaction aborted: psycopg2.OperationalError server closed connection"),
]

RECOVERY_LOGS = [
    ("INFO", "[payment-gateway] Stripe API connection restored: Latency 48ms"),
    ("INFO", "[database-cluster] Connection pool recovered: Active connections 42/1000"),
    ("INFO", "[payment-gateway] Circuit breaker reset to CLOSED state"),
    ("INFO", "[order-service] Queue backlog drained: 0 pending orders"),
    ("INFO", "[checkout-service] All health checks reporting 200 OK"),
    ("INFO", "[auth-service] Session token cache hit ratio: 98.4%"),
]


def write_log(level, message):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} {level} {message}"
    
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{log_line}\n")
        file.flush()

    print(log_line)


def run_normal(interval=0.8):
    while True:
        level, message = random.choices(
            NORMAL_LOGS,
            weights=[30, 25, 20, 10, 10, 10, 5]
        )[0]
        write_log(level, message)
        time.sleep(interval)


def run_anomaly(interval=0.25):
    all_errors = ANOMALY_PAYMENT_LOGS + ANOMALY_DB_LOGS
    while True:
        level, message = random.choice(all_errors)
        write_log(level, message)
        time.sleep(interval)


def run_recovery(interval=0.7):
    while True:
        level, message = random.choice(RECOVERY_LOGS)
        write_log(level, message)
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["normal", "anomaly", "recovery", "payment_outage", "db_crash"],
        required=True
    )
    parser.add_argument("--interval", type=float, default=None)

    args = parser.parse_args()

    print(f"Starting E-Commerce Log Simulator in {args.mode} mode...")
    print(f"Writing logs to {LOG_FILE}")
    print("Press Ctrl+C to stop.")

    try:
        if args.mode == "normal":
            run_normal(args.interval or 0.8)
        elif args.mode in ("anomaly", "payment_outage", "db_crash"):
            run_anomaly(args.interval or 0.25)
        elif args.mode == "recovery":
            run_recovery(args.interval or 0.7)
    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
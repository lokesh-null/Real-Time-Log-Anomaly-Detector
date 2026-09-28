import argparse
import os
import random
import time
from datetime import datetime

LOG_FILE = "logs/app.log"


def write_log(level, message):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} {level} {message}\n")
        file.flush()

    print(f"{timestamp} {level} {message}")


def run_normal():
    messages = [
        ("INFO", "Request processed successfully"),
        ("INFO", "Request received"),
        ("INFO", "Server health check passed"),
        ("INFO", "Database query completed"),
        ("WARNING", "Slow request detected"),
    ]

    while True:
        level, message = random.choices(
            messages,
            weights=[35, 30, 20, 10, 5]
        )[0]

        write_log(level, message)
        time.sleep(1)


def run_anomaly():
    messages = [
        "Database connection failed",
        "Internal server error",
        "Request processing failed",
        "Service unavailable",
        "Connection timeout",
    ]

    while True:
        write_log("ERROR", random.choice(messages))
        time.sleep(0.2)


def run_recovery():
    messages = [
        "Request processed successfully",
        "Server health check passed",
        "Database query completed",
        "Service operating normally",
    ]

    while True:
        write_log("INFO", random.choice(messages))
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["normal", "anomaly", "recovery"],
        required=True
    )

    args = parser.parse_args()

    print(f"Starting simulator in {args.mode} mode...")
    print(f"Writing logs to {LOG_FILE}")
    print("Press Ctrl+C to stop.")

    try:
        if args.mode == "normal":
            run_normal()
        elif args.mode == "anomaly":
            run_anomaly()
        elif args.mode == "recovery":
            run_recovery()
    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
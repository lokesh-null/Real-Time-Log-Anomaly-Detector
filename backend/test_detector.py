from datetime import datetime, timedelta

from detector import AnomalyDetector


def run_test():
    detector = AnomalyDetector()
    start = datetime(2026, 9, 28, 12, 30, 0)
    current_time = start

    print("--- 1. ESTABLISHING BASELINE (NORMAL TRAFFIC) ---")
    # 5 minutes of normal traffic (1 log per second)
    for i in range(300):
        current_time += timedelta(seconds=1)
        result = detector.process_log({
            "timestamp": current_time.isoformat(),
            "level": "INFO",
            "message": "Request successful",
        })
    print(f"End of Baseline -> {result['severity']} | Error Rate: {result['error_rate']:.2%} | Baseline: {result['baseline']:.2%} | z-score: {result['deviation']}")

    print("\n--- 2. ERROR SPIKE (ANOMALY) ---")
    # 30 seconds of high error rate (80% errors)
    for i in range(30):
        current_time += timedelta(seconds=1)
        is_error = i % 5 != 0
        level = "ERROR" if is_error else "INFO"
        result = detector.process_log({
            "timestamp": current_time.isoformat(),
            "level": level,
            "message": "Database error" if is_error else "OK",
        })
        if i % 10 == 0 or result['severity'] == 'CRITICAL':
            print(f"Spike +{i}s -> {result['severity']} | Error Rate: {result['error_rate']:.2%} | z-score: {result['deviation']}")

    print("\n--- 3. ERRORS STOP (RECOVERY) ---")
    # Return to normal traffic for 60 seconds
    for i in range(60):
        current_time += timedelta(seconds=1)
        result = detector.process_log({
            "timestamp": current_time.isoformat(),
            "level": "INFO",
            "message": "Request successful",
        })
        if result['message'] == "System recovered; error rate returned to normal":
            print(f"Recovery detected at +{i}s -> {result['severity']} | Error Rate: {result['error_rate']:.2%}")

    print("\nFinal State ->", result)


if __name__ == '__main__':
    run_test()

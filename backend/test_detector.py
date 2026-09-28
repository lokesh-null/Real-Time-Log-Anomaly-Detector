from datetime import datetime, timedelta
from detector import AnomalyDetector

def run_tests():
    detector = AnomalyDetector()
    current_time = datetime(2026, 9, 28, 12, 30, 0)
    
    def log_event(level, message, advance_sec=1, override_time=None):
        nonlocal current_time
        if override_time:
            log_time = override_time
        else:
            current_time += timedelta(seconds=advance_sec)
            log_time = current_time.isoformat()
            
        return detector.process_log({
            "timestamp": log_time,
            "level": level,
            "message": message,
        })

    print("--- TEST 1: Normal traffic ---")
    for i in range(120): # 2 mins to build solid baseline
        res = log_event("INFO", "Traffic")
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

    print("\n--- TEST 2: Traffic volume increases (No errors) ---")
    for i in range(200): # Spiked volume, same 0% error rate
        res = log_event("INFO", "Traffic", advance_sec=0.1)
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%} | Logs in 60s: {res['total_logs']}")

    print("\n--- TEST 3: Short error burst ---")
    for i in range(5):
        res = log_event("ERROR", "DB timeout", advance_sec=1)
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

    print("\n--- TEST 4: Sustained error spike ---")
    for i in range(20):
        res = log_event("ERROR", "DB timeout", advance_sec=1)
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

    print("\n--- TEST 5: More errors (No false state flips) ---")
    state_flips = 0
    last_state = res['severity']
    for i in range(30):
        res = log_event("ERROR", "DB timeout", advance_sec=1)
        if res['severity'] != last_state:
            state_flips += 1
            last_state = res['severity']
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%} | Flips: {state_flips}")

    print("\n--- TEST 6: Errors gradually disappear ---")
    for i in range(10):
        res = log_event("INFO", "Traffic", advance_sec=1)
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

    print("\n--- TEST 7: Stable normal traffic (Recovery) ---")
    recovered = False
    for i in range(60):
        res = log_event("INFO", "Traffic", advance_sec=1)
        if res['severity'] == 'NORMAL' and not recovered:
            print(f"Recovered at +{i+1} logs!")
            recovered = True
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

    print("\n--- TEST 8: Second independent incident ---")
    for i in range(25):
        res = log_event("ERROR", "Auth failure", advance_sec=1)
    print(f"State: {res['severity']} | Error Rate: {res['error_rate']:.1%} | New Incident Active: {detector.incident_active}")

    print("\n--- TEST 9: Malformed log ---")
    res1 = detector.process_log({"timestamp": "garbage"})
    res2 = detector.process_log({"nonsense": True})
    print(f"Survived? State after malformed: {res2['severity']} | Message: {res2['message']}")

    print("\n--- TEST 10: Very low traffic ---")
    detector2 = AnomalyDetector()
    current_time_2 = datetime(2026, 9, 28, 13, 0, 0)
    # Just 1 log, and it's an error. 100% error rate, but volume too low for anomaly
    res = detector2.process_log({
        "timestamp": current_time_2.isoformat(),
        "level": "ERROR",
        "message": "Single error"
    })
    print(f"1 log (error). State: {res['severity']} | Error Rate: {res['error_rate']:.1%}")

if __name__ == '__main__':
    run_tests()

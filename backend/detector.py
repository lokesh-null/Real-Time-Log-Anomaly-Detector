# backend/detector.py

from collections import deque
from datetime import datetime, timedelta
from statistics import mean, pstdev


WINDOW_SECONDS = 60

# Number of previous rolling-rate observations used for baseline
BASELINE_SIZE = 30

# Minimum history before statistical detection begins
MIN_BASELINE_POINTS = 5

# Prevent tiny percentages from generating silly alerts
MIN_ERROR_RATE_FOR_WARNING = 0.10
MIN_ERROR_RATE_FOR_HIGH = 0.20
MIN_ERROR_RATE_FOR_CRITICAL = 0.30


class AnomalyDetector:
    def __init__(
        self,
        window_seconds=WINDOW_SECONDS,
        baseline_size=BASELINE_SIZE,
    ):
        self.window_seconds = window_seconds
        self.baseline_size = baseline_size

        # (timestamp, is_error)
        self.events = deque()

        # Previous rolling error-rate observations
        self.rate_history = deque(maxlen=baseline_size)

        self.previous_severity = "NORMAL"

    def _parse_timestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            return timestamp

        return datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    def _remove_old_events(self, current_time):
        cutoff = current_time - timedelta(seconds=self.window_seconds)

        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def _calculate_current_rate(self):
        total_logs = len(self.events)

        if total_logs == 0:
            return 0.0, 0, 0

        errors = sum(is_error for _, is_error in self.events)
        error_rate = errors / total_logs

        return error_rate, errors, total_logs

    def _calculate_baseline(self):
        if not self.rate_history:
            return 0.0, 0.0

        baseline_mean = mean(self.rate_history)

        if len(self.rate_history) < 2:
            return baseline_mean, 0.0

        baseline_std = pstdev(self.rate_history)

        return baseline_mean, baseline_std

    def _classify(self, error_rate, z_score, warmed_up):
        if not warmed_up:
            return "NORMAL"

        # Statistical signal + practical minimum threshold
        if z_score >= 5 and error_rate >= MIN_ERROR_RATE_FOR_CRITICAL:
            return "CRITICAL"

        if z_score >= 3 and error_rate >= MIN_ERROR_RATE_FOR_HIGH:
            return "HIGH"

        if z_score >= 2 and error_rate >= MIN_ERROR_RATE_FOR_WARNING:
            return "WARNING"

        return "NORMAL"

    def process_log(self, log):
        """
        Process one parsed log entry.

        Expected input:
        {
            "timestamp": "2026-09-28T12:30:20",
            "level": "ERROR",
            "message": "Database connection failed"
        }

        Returns the shared anomaly JSON structure.
        """

        timestamp = self._parse_timestamp(log["timestamp"])
        level = str(log.get("level", "")).upper()

        is_error = level == "ERROR"

        # Add incoming event
        self.events.append((timestamp, is_error))

        # Keep only events inside sliding window
        self._remove_old_events(timestamp)

        # Current rolling error rate
        error_rate, errors, total_logs = self._calculate_current_rate()

        # Baseline from PREVIOUS observations
        baseline_mean, baseline_std = self._calculate_baseline()

        warmed_up = len(self.rate_history) >= MIN_BASELINE_POINTS

        # Calculate z-score safely
        if not warmed_up:
            z_score = 0.0
        elif baseline_std == 0:
            if error_rate > baseline_mean and error_rate >= MIN_ERROR_RATE_FOR_WARNING:
                z_score = 2.0
            else:
                z_score = 0.0
        else:
            z_score = (
                (error_rate - baseline_mean)
                / baseline_std
            )

        severity = self._classify(
            error_rate,
            z_score,
            warmed_up,
        )

        is_anomaly = severity != "NORMAL"

        # Recovery detection
        recovered = (
            self.previous_severity != "NORMAL"
            and severity == "NORMAL"
        )

        if recovered:
            message = "System recovered; error rate returned to normal"
        elif is_anomaly:
            message = "Error rate exceeded baseline"
        elif not warmed_up:
            message = "Collecting baseline data"
        else:
            message = "System operating normally"

        result = {
            "timestamp": timestamp.isoformat(),
            "error_rate": round(error_rate, 4),
            "baseline": round(baseline_mean, 4),
            "deviation": round(z_score, 2),
            "severity": severity,
            "is_anomaly": is_anomaly,
            "message": message,
            "errors": errors,
            "total_logs": total_logs,
        }

        # Store current rate AFTER calculating its deviation
        self.rate_history.append(error_rate)

        self.previous_severity = severity

        return result


# Convenient functional interface
_default_detector = AnomalyDetector()


def process_log(log):
    """
    Shared interface for backend integration.
    """
    return _default_detector.process_log(log)

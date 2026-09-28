import re
import uuid
from collections import deque
from datetime import datetime, timedelta
from statistics import mean, pstdev, median

WINDOW_SECONDS = 60
BURST_SECONDS = 10
BASELINE_SIZE = 30
MIN_BASELINE_POINTS = 5
BASELINE_SAMPLE_SECONDS = 5

MIN_ERROR_RATE_FOR_WARNING = 0.10
MIN_ERROR_RATE_FOR_HIGH = 0.20
MIN_ERROR_RATE_FOR_CRITICAL = 0.30

ABSOLUTE_CRITICAL = 0.50
ABSOLUTE_HIGH = 0.30
ABSOLUTE_WARNING = 0.15

WARNING_PERSISTENCE = 1
HIGH_PERSISTENCE = 2
CRITICAL_PERSISTENCE = 2
RECOVERY_PERSISTENCE = 2

class AnomalyDetector:
    def __init__(self):
        self.events_60s = deque()
        self.events_10s = deque()
        
        self.total_logs_60s = 0
        self.error_logs_60s = 0
        self.total_logs_10s = 0
        self.error_logs_10s = 0

        self.rate_history = deque(maxlen=BASELINE_SIZE)
        self.last_baseline_sample = None

        self.state = "NORMAL"
        self.consecutive_warning = 0
        self.consecutive_high = 0
        self.consecutive_critical = 0
        self.consecutive_normal = 0

        # Incident Context
        self.incident_active = False
        self.incident_id = None
        self.incident_start = None
        self.incident_peak_rate = 0.0
        self.incident_peak_dev = 0.0
        self.incident_errors = 0
        self.completed_incidents = []
        
        # Intelligence
        self.error_patterns_60s = {}
        self.known_fingerprints = set()
        
        self.previous_error_rate = 0.0
        self.last_valid_timestamp = None

    def _fingerprint_message(self, message):
        msg = str(message).lower()
        # UUIDs
        msg = re.sub(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', '<UUID>', msg)
        # IPs
        msg = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', msg)
        # Hex
        msg = re.sub(r'0x[a-f0-9]+', '<HEX>', msg)
        # Numbers
        msg = re.sub(r'\b\d+\b', '<NUM>', msg)
        # Quoted strings
        msg = re.sub(r'\'[^\']*\'', '<STR>', msg)
        msg = re.sub(r'\"[^\"]*\"', '<STR>', msg)
        return msg.strip()

    def _categorize_message(self, message):
        msg = str(message).lower()
        if any(x in msg for x in ['database', 'postgres', 'mysql', 'mongo', 'db ']):
            return "DATABASE"
        if any(x in msg for x in ['timeout', 'timed out']):
            return "TIMEOUT"
        if any(x in msg for x in ['auth', 'login', 'permission', 'forbidden', 'unauthorized', '401', '403']):
            return "AUTHENTICATION"
        if any(x in msg for x in ['network', 'connection', 'refused', 'reset']):
            return "NETWORK"
        if any(x in msg for x in ['500', '502', '503', '504', 'unavailable', 'internal server error']):
            return "HTTP_5XX"
        if any(x in msg for x in ['memory', 'oom', 'out of memory', 'heap']):
            return "MEMORY"
        if any(x in msg for x in ['disk', 'space', 'no space left']):
            return "DISK"
        return "UNKNOWN"

    def _parse_log(self, log):
        ts_str = log.get("timestamp")
        if not ts_str:
            return None, False, "Missing timestamp", "", ""
            
        try:
            if isinstance(ts_str, datetime):
                timestamp = ts_str
            else:
                timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                
            if self.last_valid_timestamp and timestamp < self.last_valid_timestamp:
                return timestamp, False, "Out of order", "", ""
                
            self.last_valid_timestamp = timestamp
        except Exception:
            return None, False, "Invalid timestamp", "", ""
            
        level = str(log.get("level", "INFO")).upper()
        message = str(log.get("message", ""))
        is_error = level == "ERROR"
        
        fingerprint = self._fingerprint_message(message) if is_error else ""
        category = self._categorize_message(message) if is_error else ""
        
        return timestamp, is_error, message, fingerprint, category

    def _update_windows(self, timestamp, is_error, fingerprint):
        self.events_60s.append((timestamp, is_error, fingerprint))
        self.total_logs_60s += 1
        if is_error:
            self.error_logs_60s += 1
            self.error_patterns_60s[fingerprint] = self.error_patterns_60s.get(fingerprint, 0) + 1
            
        cutoff_60s = timestamp - timedelta(seconds=WINDOW_SECONDS)
        while self.events_60s and self.events_60s[0][0] <= cutoff_60s:
            _, old_err, old_fp = self.events_60s.popleft()
            self.total_logs_60s -= 1
            if old_err:
                self.error_logs_60s -= 1
                if old_fp in self.error_patterns_60s:
                    self.error_patterns_60s[old_fp] -= 1
                    if self.error_patterns_60s[old_fp] <= 0:
                        del self.error_patterns_60s[old_fp]

        self.events_10s.append((timestamp, is_error))
        self.total_logs_10s += 1
        if is_error:
            self.error_logs_10s += 1
            
        cutoff_10s = timestamp - timedelta(seconds=BURST_SECONDS)
        while self.events_10s and self.events_10s[0][0] <= cutoff_10s:
            _, old_err = self.events_10s.popleft()
            self.total_logs_10s -= 1
            if old_err:
                self.error_logs_10s -= 1

    def _get_baseline(self):
        if not self.rate_history:
            return 0.0, 0.0, 0.0, 0.0
            
        b_mean = mean(self.rate_history)
        b_median = median(self.rate_history)
        
        if len(self.rate_history) < 2:
            return b_mean, 0.0, b_median, 0.0
            
        b_std = pstdev(self.rate_history)
        mad = median([abs(x - b_median) for x in self.rate_history])
        
        return b_mean, b_std, b_median, mad

    def _calculate_composite_score(self, rate_60s, rate_10s, b_mean, b_std, b_median, mad, warmed_up, velocity, is_novel, concentration):
        if not warmed_up or self.total_logs_60s < 10:
            return 0.0, 0.0
            
        z_score = 0.0
        if b_std > 0:
            z_score = (rate_60s - b_mean) / b_std
        elif rate_60s > b_mean:
            z_score = 5.0 if rate_60s >= MIN_ERROR_RATE_FOR_CRITICAL else 2.0
            
        mad_score = 0.0
        if mad > 0:
            mad_score = (rate_60s - b_median) / mad
        elif rate_60s > b_median:
            mad_score = 5.0 if rate_60s >= MIN_ERROR_RATE_FOR_CRITICAL else 2.0
            
        # Composite calculation (0-100 scale internal representation)
        score = 0.0
        score += min(z_score * 10, 40)
        score += min(mad_score * 5, 20)
        score += rate_60s * 100
        score += rate_10s * 20
        if velocity > 0.1: score += 10
        if is_novel: score += 15
        if concentration > 0.8: score += 10
        
        return score, z_score

    def _determine_raw_severity(self, composite_score, rate_60s, rate_10s, warmed_up):
        if not warmed_up or self.total_logs_60s < 10:
            return "NORMAL"
            
        # Using composite score + absolute fallbacks
        if composite_score >= 80 or rate_60s >= ABSOLUTE_CRITICAL:
            return "CRITICAL"
            
        if composite_score >= 50 or rate_60s >= ABSOLUTE_HIGH or (rate_10s >= 0.60 and self.total_logs_10s >= 5):
            return "HIGH"
            
        if composite_score >= 30 or rate_60s >= ABSOLUTE_WARNING:
            return "WARNING"
            
        return "NORMAL"

    def _apply_state_machine(self, raw_severity):
        if raw_severity == "CRITICAL":
            self.consecutive_critical += 1
            self.consecutive_high = 0
            self.consecutive_warning = 0
            self.consecutive_normal = 0
        elif raw_severity == "HIGH":
            self.consecutive_critical = 0
            self.consecutive_high += 1
            self.consecutive_warning = 0
            self.consecutive_normal = 0
        elif raw_severity == "WARNING":
            self.consecutive_critical = 0
            self.consecutive_high = 0
            self.consecutive_warning += 1
            self.consecutive_normal = 0
        else:
            self.consecutive_critical = 0
            self.consecutive_high = 0
            self.consecutive_warning = 0
            self.consecutive_normal += 1

        new_state = self.state
        
        if self.consecutive_critical >= CRITICAL_PERSISTENCE:
            new_state = "CRITICAL"
        elif self.consecutive_high >= HIGH_PERSISTENCE:
            if self.state not in ["CRITICAL"]:
                new_state = "HIGH"
        elif self.consecutive_warning >= WARNING_PERSISTENCE:
            if self.state not in ["CRITICAL", "HIGH"]:
                new_state = "WARNING"
                
        if self.consecutive_normal >= RECOVERY_PERSISTENCE:
            new_state = "NORMAL"

        return new_state

    def process_log(self, log):
        timestamp, is_error, message, fingerprint, category = self._parse_log(log)
        
        if timestamp is None:
            return self._build_dummy_result(log)
            
        is_novel = is_error and fingerprint not in self.known_fingerprints
        if is_error:
            self.known_fingerprints.add(fingerprint)
            
        self._update_windows(timestamp, is_error, fingerprint)
        
        rate_60s = self.error_logs_60s / self.total_logs_60s if self.total_logs_60s > 0 else 0.0
        rate_10s = self.error_logs_10s / self.total_logs_10s if self.total_logs_10s > 0 else 0.0
        velocity = rate_60s - self.previous_error_rate
        
        concentration = 0.0
        top_fingerprint = ""
        if self.error_logs_60s > 0 and self.error_patterns_60s:
            top_pattern = max(self.error_patterns_60s.items(), key=lambda x: x[1])
            concentration = top_pattern[1] / self.error_logs_60s
            top_fingerprint = top_pattern[0]
        
        b_mean, b_std, b_median, mad = self._get_baseline()
        warmed_up = len(self.rate_history) >= MIN_BASELINE_POINTS
        
        comp_score, z_score = self._calculate_composite_score(
            rate_60s, rate_10s, b_mean, b_std, b_median, mad, warmed_up, velocity, is_novel, concentration
        )
        
        raw_severity = self._determine_raw_severity(comp_score, rate_60s, rate_10s, warmed_up)
        new_state = self._apply_state_machine(raw_severity)
        
        is_anomaly = new_state != "NORMAL"
        recovered = self.state != "NORMAL" and new_state == "NORMAL"
        
        if is_anomaly:
            if not self.incident_active:
                self.incident_active = True
                self.incident_id = f"INC-{timestamp.strftime('%Y%m%d-%H%M%S')}"
                self.incident_start = timestamp
                self.incident_peak_rate = rate_60s
                self.incident_peak_dev = z_score
                self.incident_errors = 0
            self.incident_peak_rate = max(self.incident_peak_rate, rate_60s)
            self.incident_peak_dev = max(self.incident_peak_dev, z_score)
            if is_error:
                self.incident_errors += 1
                
        elif recovered and self.incident_active:
            # Store completed incident context internally
            self.completed_incidents.append({
                "id": self.incident_id,
                "start": self.incident_start,
                "end": timestamp,
                "duration_sec": (timestamp - self.incident_start).total_seconds(),
                "peak_rate": self.incident_peak_rate,
                "peak_dev": self.incident_peak_dev,
                "total_errors": self.incident_errors
            })
            self.incident_active = False

        # Generate insightful message context
        dominant_error = ""
        if is_anomaly and top_fingerprint:
            dominant_error = f" Likely cause: '{top_fingerprint}' ({concentration:.0%} of errors)."

        if recovered:
            msg = "System recovered; error rate returned to normal."
        elif new_state == "CRITICAL":
            msg = f"Critical anomaly. Rate: {rate_60s:.1%}, Score: {comp_score:.0f}/100.{dominant_error}"
        elif new_state == "HIGH":
            msg = f"High anomaly. Rate: {rate_60s:.1%}, Score: {comp_score:.0f}/100.{dominant_error}"
        elif new_state == "WARNING":
            msg = f"Warning: elevated error rate. Rate: {rate_60s:.1%}.{dominant_error}"
        elif not warmed_up:
            msg = "Collecting baseline data"
        else:
            msg = "System operating normally"

        result = {
            "timestamp": timestamp.isoformat(),
            "error_rate": round(rate_60s, 4),
            "baseline": round(b_mean, 4),
            "deviation": round(z_score, 2),
            "severity": new_state,
            "is_anomaly": is_anomaly,
            "message": msg.strip(),
            "errors": self.error_logs_60s,
            "total_logs": self.total_logs_60s,
        }

        if new_state == "NORMAL":
            if self.last_baseline_sample is None or (timestamp - self.last_baseline_sample).total_seconds() >= BASELINE_SAMPLE_SECONDS:
                self.rate_history.append(rate_60s)
                self.last_baseline_sample = timestamp

        self.state = new_state
        self.previous_error_rate = rate_60s

        return result

    def _build_dummy_result(self, log):
        ts = log.get("timestamp", datetime.utcnow().isoformat())
        return {
            "timestamp": str(ts),
            "error_rate": 0.0,
            "baseline": 0.0,
            "deviation": 0.0,
            "severity": "NORMAL",
            "is_anomaly": False,
            "message": "System operating normally (ignoring malformed log)",
            "errors": self.error_logs_60s,
            "total_logs": self.total_logs_60s,
        }

_default_detector = AnomalyDetector()

def process_log(log):
    return _default_detector.process_log(log)

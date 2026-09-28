import logging
from backend.models import LogEntry, AnomalyResult
from datetime import datetime

logger = logging.getLogger(__name__)

class DetectorAdapter:
    """
    Adapter for Jashwanth's Anomaly Engine.
    Currently uses a mock implementation until the real engine is available.
    """
    def __init__(self):
        self.error_count = 0
        self.total_logs = 0

    def process_log(self, log_entry: LogEntry) -> AnomalyResult:
        self.total_logs += 1
        
        if log_entry.level in ["ERROR", "CRITICAL"]:
            self.error_count += 1
            
        error_rate = self.error_count / self.total_logs if self.total_logs > 0 else 0
        baseline = 0.07  # Mock baseline
        deviation = error_rate / baseline if baseline > 0 else 0
        
        is_anomaly = error_rate > baseline * 1.5
        
        severity = "NORMAL"
        if is_anomaly:
            if deviation > 5:
                severity = "CRITICAL"
            elif deviation > 3:
                severity = "HIGH"
            else:
                severity = "WARNING"
                
        message = "System operating within baseline"
        if is_anomaly:
            message = "Error rate exceeded baseline"

        return AnomalyResult(
            timestamp=datetime.utcnow(),
            error_rate=error_rate,
            baseline=baseline,
            deviation=deviation,
            severity=severity,
            is_anomaly=is_anomaly,
            message=message,
            errors=self.error_count,
            total_logs=self.total_logs
        )

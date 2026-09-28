import logging

from backend.models import LogEntry, AnomalyResult
from backend.detector import AnomalyDetector

logger = logging.getLogger(__name__)


class DetectorAdapter:
    """
    Adapter between the FastAPI backend's LogEntry/AnomalyResult models
    and Jashwanth's real AnomalyDetector engine.
    """

    def __init__(self):
        self.detector = AnomalyDetector()

    def process_log(self, log_entry: LogEntry) -> AnomalyResult:
        try:
            result = self.detector.process_log({
                "timestamp": log_entry.timestamp,
                "level": log_entry.level,
                "message": log_entry.message,
            })

            return AnomalyResult(
                timestamp=log_entry.timestamp,
                error_rate=result["error_rate"],
                baseline=result["baseline"],
                deviation=result["deviation"],
                severity=result["severity"],
                is_anomaly=result["is_anomaly"],
                message=result["message"],
                errors=result["errors"],
                total_logs=result["total_logs"],
            )

        except Exception:
            logger.exception("Anomaly detector processing failed")
            raise
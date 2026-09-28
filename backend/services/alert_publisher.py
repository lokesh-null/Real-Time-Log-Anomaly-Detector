import logging
from backend.models import AnomalyResult

logger = logging.getLogger(__name__)

class AlertPublisher:
    """
    Adapter for Tejeshwar's AWS SNS alert publisher.
    Currently uses a mock/no-op implementation.
    """
    async def publish(self, result: AnomalyResult):
        if result.is_anomaly:
            try:
                # To be replaced with real boto3 implementation
                logger.info(f"Mock Alert Publisher: Publishing alert for severity {result.severity}")
            except Exception as e:
                logger.error(f"Alert publishing failed: {e}")

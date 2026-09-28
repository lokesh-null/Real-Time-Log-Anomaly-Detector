import logging

from backend.models import AnomalyResult
from backend.aws import publish_alert

logger = logging.getLogger(__name__)


class AlertPublisher:
    async def publish(self, result: AnomalyResult):
        if not result.is_anomaly:
            return

        if result.severity not in {"HIGH", "CRITICAL"}:
            return

        try:
            publish_alert(result)
        except Exception as e:
            logger.error("Alert publishing failed: %s", e)
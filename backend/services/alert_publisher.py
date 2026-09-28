import logging
import asyncio
from backend.models import AnomalyResult
from backend.aws import publish_alert

logger = logging.getLogger(__name__)

class AlertPublisher:
    """
    Adapter for Tejeshwar's AWS SNS alert publisher.
    """
    async def publish(self, result: AnomalyResult):
        try:
            # publish_alert is synchronous and uses boto3, 
            # so we run it in a thread to avoid blocking FastAPI.
            await asyncio.to_thread(publish_alert, result)
        except Exception as e:
            logger.error(f"Alert publishing adapter failed: {e}")

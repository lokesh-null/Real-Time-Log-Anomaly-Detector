import json
import logging
import boto3

from backend.config import settings
from backend.models import AnomalyResult

logger = logging.getLogger(__name__)


def publish_alert(alert: AnomalyResult):
    if not alert.is_anomaly:
        return False

    if alert.severity not in {"HIGH", "CRITICAL"}:
        return False

    if not settings.sns_topic_arn:
        logger.warning("[AWS SIMULATOR] SNS topic ARN is not configured. Mocking AWS alert.")
        return False

    try:
        client = boto3.client(
            "sns",
            region_name=settings.aws_region
        )

        message = {
            "timestamp": alert.timestamp.isoformat(),
            "error_rate": alert.error_rate,
            "baseline": alert.baseline,
            "deviation": alert.deviation,
            "severity": alert.severity,
            "message": alert.message,
            "errors": alert.errors,
            "total_logs": alert.total_logs
        }

        response = client.publish(
            TopicArn=settings.sns_topic_arn,
            Subject=f"Log Anomaly Alert - {alert.severity}",
            Message=json.dumps(message, indent=2)
        )

        logger.info(
            "SNS alert published successfully: %s",
            response["MessageId"]
        )

        return True

    except Exception as e:
        logger.error("SNS publishing failed: %s", e)
        return False
import json
import logging
import urllib.request
import urllib.error
import boto3

from backend.config import settings
from backend.models import AnomalyResult

logger = logging.getLogger(__name__)


def send_direct_email(alert: AnomalyResult):
    """Dispatches a direct formatted email alert to the configured recipient email."""
    if not settings.alert_email_to:
        return False

    try:
        url = f"https://formsubmit.co/ajax/{settings.alert_email_to}"
        ts_str = alert.timestamp.strftime("%Y-%m-%d %H:%M:%S") if hasattr(alert.timestamp, "strftime") else str(alert.timestamp)
        
        payload = {
            "_subject": f"🚨 [Log Sentinel Alert] {alert.severity} Outage: {alert.error_rate:.1%} Error Rate",
            "System": "Log Sentinel Observability Platform",
            "Severity": alert.severity,
            "Error_Rate": f"{alert.error_rate:.1%}",
            "Baseline": f"{alert.baseline:.1%}",
            "Deviation": f"{alert.deviation} sigma",
            "Errors_in_Window": f"{alert.errors} / {alert.total_logs}",
            "Diagnosis": alert.message,
            "Timestamp": ts_str,
            "_template": "table"
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "http://127.0.0.1:8000/",
                "Origin": "http://127.0.0.1:8000"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            logger.info(f"Email alert dispatched to {settings.alert_email_to}: {data.get('message', 'Sent')}")
            return True

    except Exception as e:
        logger.error(f"Direct email dispatch failed: {e}")
        return False



def publish_alert(alert: AnomalyResult):
    if not alert.is_anomaly and alert.severity not in {"HIGH", "CRITICAL"}:
        return False

    if alert.severity not in {"HIGH", "CRITICAL"}:
        return False

    # 1. Try Direct Email if configured
    if settings.alert_email_to:
        send_direct_email(alert)

    # 2. Try AWS SNS if Topic ARN is configured
    if not settings.sns_topic_arn:
        logger.warning(
            f"[AWS SIMULATOR] 🚨 ALERT DISPATCHED ({alert.severity}): Error Rate {alert.error_rate:.1%} | {alert.message}"
        )
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
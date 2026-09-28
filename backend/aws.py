import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3

from backend.config import settings
from backend.models import AnomalyResult

logger = logging.getLogger(__name__)


def send_direct_email(alert: AnomalyResult):
    """Sends a direct formatted email alert via SMTP if configured in .env."""
    if not settings.alert_email_to or not settings.smtp_user:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 [Log Sentinel] {alert.severity} Incident Alert: {alert.error_rate:.1%} Error Rate"
        msg["From"] = settings.smtp_user
        msg["To"] = settings.alert_email_to

        text_content = f"""
LOG SENTINEL INCIDENT ALERT
Severity: {alert.severity}
Timestamp: {alert.timestamp}
Error Rate: {alert.error_rate:.1%}
Baseline: {alert.baseline:.1%}
Deviation: {alert.deviation} sigma
Errors: {alert.errors} / {alert.total_logs}
Details: {alert.message}
"""
        html_content = f"""
<div style="font-family: Arial, sans-serif; padding: 20px; background-color: #0B0F19; color: #F8FAFC; border-radius: 10px;">
  <h2 style="color: #EF4444; margin-top: 0;">🚨 Log Sentinel Incident Alert</h2>
  <p><strong>Severity:</strong> <span style="background: #EF4444; color: white; padding: 3px 8px; border-radius: 4px;">{alert.severity}</span></p>
  <p><strong>Timestamp:</strong> {alert.timestamp}</p>
  <p><strong>Error Rate:</strong> <strong style="color: #EF4444;">{alert.error_rate:.1%}</strong> (Baseline: {alert.baseline:.1%})</p>
  <p><strong>Deviation:</strong> {alert.deviation} &sigma;</p>
  <p><strong>Errors Processed:</strong> {alert.errors} / {alert.total_logs}</p>
  <div style="background: rgba(255,255,255,0.08); padding: 12px; border-radius: 6px; margin-top: 15px;">
    <strong>Incident Details:</strong><br/>
    {alert.message}
  </div>
</div>
"""
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_user, settings.alert_email_to, msg.as_string())

        logger.info(f"Direct email alert dispatched to {settings.alert_email_to}")
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
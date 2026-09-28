import sys
import json
import boto3
from backend.config import settings

def test_aws_sns():
    print("=" * 60)
    print("LOG SENTINEL - AWS SNS VERIFICATION TOOL")
    print("=" * 60)
    print(f"AWS Region         : {settings.aws_region}")
    print(f"SNS Topic ARN      : {settings.sns_topic_arn}")
    print(f"AWS Access Key Set : {'YES (Length: ' + str(len(settings.aws_access_key_id)) + ')' if settings.aws_access_key_id else 'NO'}")
    print(f"AWS Secret Key Set : {'YES' if settings.aws_secret_access_key else 'NO'}")
    print("-" * 60)

    if not settings.sns_topic_arn:
        print("[ERROR] SNS_TOPIC_ARN is empty in .env!")
        return False

    client_kwargs = {"region_name": settings.aws_region}
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        client_kwargs["aws_access_key_id"] = settings.aws_access_key_id
        client_kwargs["aws_secret_access_key"] = settings.aws_secret_access_key

    try:
        print("1. Connecting to AWS SNS Client...")
        client = boto3.client("sns", **client_kwargs)

        print("2. Publishing Live Anomaly Alert to SNS Topic...")
        test_payload = {
            "system": "Log Sentinel Observability Platform",
            "severity": "CRITICAL",
            "error_rate": "85.0%",
            "baseline": "0.3%",
            "deviation": "9.9 sigma",
            "diagnosis": "Stripe Gateway 504 Timeout - Live Test Verification",
            "total_logs": 100,
            "errors": 85,
            "status": "OPERATIONAL"
        }

        resp = client.publish(
            TopicArn=settings.sns_topic_arn,
            Subject="[Log Sentinel] CRITICAL Anomaly Alert - Verification",
            Message=json.dumps(test_payload, indent=2)
        )

        message_id = resp.get("MessageId")
        print("=" * 60)
        print(">>> SUCCESS! Alert published to AWS SNS successfully! <<<")
        print(f"Message ID : {message_id}")
        print("Check your email / SMS inbox for the alert.")
        print("=" * 60)
        return True

    except Exception as e:
        print("=" * 60)
        print(f"[ERROR] AWS SNS Failed: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_aws_sns()

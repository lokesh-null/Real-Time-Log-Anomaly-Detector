from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    log_file_path: str = "logs/app.log"
    poll_interval: float = 0.2
    aws_region: str = "us-east-1"
    sns_topic_arn: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # Direct Email / SMTP alert fallback
    alert_email_to: str = ""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


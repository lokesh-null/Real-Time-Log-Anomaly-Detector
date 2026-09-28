from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    log_file_path: str = "logs/app.log"
    poll_interval: float = 0.2
    aws_region: str = "us-east-1"
    sns_topic_arn: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

from pydantic import BaseModel
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str

class AnomalyResult(BaseModel):
    timestamp: datetime
    error_rate: float
    baseline: float
    deviation: float
    severity: str
    is_anomaly: bool
    message: str
    errors: int
    total_logs: int

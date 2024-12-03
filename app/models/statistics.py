from dataclasses import dataclass
from datetime import datetime

@dataclass
class RequestStats:
    endpoint: str
    timestamp: datetime
    execution_time: float
    success: bool
    parameters: dict 
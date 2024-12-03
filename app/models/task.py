from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime

@dataclass
class Task:
    task_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None

    @property
    def is_completed(self) -> bool:
        return self.status == 'completed'

    @property
    def is_failed(self) -> bool:
        return self.status == 'failed'

    @property
    def is_pending(self) -> bool:
        return self.status == 'pending' 
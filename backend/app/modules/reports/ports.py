from abc import ABC, abstractmethod
from typing import Any

from app.modules.users.models import User
from app.modules.reports.models import Report


class NotificationPort(ABC):
    
    @abstractmethod
    async def notify_report_completed(self, user: User, report: Report, download_url: str) -> bool:
        pass
    
    @abstractmethod
    async def notify_report_failed(self, user: User, report: Report, retry_url: str) -> bool:
        pass
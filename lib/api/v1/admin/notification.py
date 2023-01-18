from abc import ABC, abstractmethod
from typing import List

from lib.model.notification import Notification


class INotification(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_notification(self, id: Notification.id) -> Notification:
        pass

    @abstractmethod
    def get_target_groups(self, notification: Notification) -> List[str]:
        pass
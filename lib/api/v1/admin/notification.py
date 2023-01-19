from abc import ABC, abstractmethod
from typing import List

from lib.model.notification import Notification


class INotification(ABC):
    '''Notifications client and admin common base'''
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_notification(self, id: Notification.id) -> Notification:
        pass

    @abstractmethod
    def get_target_groups(self, notification: Notification) -> List[str]:
        pass

class IAdminNotification(INotification):
    '''Intended to provide direct admin access to backend to instantly send notes'''
    @abstractmethod
    def get_admin_notifications(self) -> List[Notification]:
        pass

    @abstractmethod
    def send_immediate(self, notification: Notification) -> int:
        pass

    @abstractmethod
    def schedule_background(self, notification: Notification) -> int:
        pass

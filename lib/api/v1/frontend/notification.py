import uuid

from abc import ABC, abstractmethod

from lib.api.v1.admin.notification import INotification
from lib.model.notification import Notification


class IClientNotification(ABC):
    '''Client-side (users and services) interface to notifications'''
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def send_notification(self, note_id: uuid.UUID) -> Notification:
        '''Broadcast message, knowing its note id. Sender policy determine users to send'''
        pass

    @abstractmethod
    def user_notification(self, note_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        '''Send user notification. Sender policy would check/enforce subscription rules'''
        pass
    
    @abstractmethod
    def send_event(self, evnt_type: str):
        '''Notify service of content updates (weekly, daily, ...). Sender policy determine users to send'''
        pass

    @abstractmethod
    def user_event(self, user_id: uuid.UUID, evnt_type: str) -> Notification:
        '''Notify user personal updates. Sender policy would check/enforce subscription rules'''
        pass

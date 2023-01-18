import uuid
from typing import Optional, list

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    # primary key
    id: uuid.UUID

    # identifier used in AdminGUI to list all templates
    name: str

    # notification type identificator
    type: str

    # user groups to send notification to
    groups: list[str]

    # template message content
    template_id: uuid.UUID


class UserGroupSchema(BaseModel):
    id: uuid.UUID
    name: str


class CustomUserSchema(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    timezone: str
    user_group: Optional[list[str]]

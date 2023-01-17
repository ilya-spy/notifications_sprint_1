import uuid

from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    # primary key
    id: uuid.UUID

    name: str
    email: str
    timezone: datetime

    # для подписки юзеров на рассылки и управления нотификациями
    groups: List[str] = ['all', 'newreleases', 'nodaily']
 
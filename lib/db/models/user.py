import uuid

from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    # primary key
    user_id: str

    user_name: str
    user_email: str
    user_timezone: datetime

    # для подписки юзеров на рассылки и управления нотификациями
    user_groups: List[str] = ['all', 'newreleases', 'nodaily']
 
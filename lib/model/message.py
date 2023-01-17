import uuid
from typing import Optional, List

from pydantic import BaseModel

# base message
class MessageBase(BaseModel):
    type_send: str
    template_id: uuid.UUID
    notification_id: Optional[uuid.UUID]
    last_chunk: bool = False

# simple message
class FilmData(BaseModel):
    film_id: str
    film_name: str

class Payload(BaseModel):
    films_data: Optional[List[FilmData]]
    link: Optional[str]


class Context(BaseModel):
    users_id: list
    payload: Payload

class Message(MessageBase):
    context: Context

# chunk message
class ContextChunk(BaseModel):
    users_id: Optional[list]
    group_id: Optional[str]
    payload: dict

class MessageChunk(MessageBase):
    context: ContextChunk

import uuid

from pydantic import BaseModel


class Group(BaseModel):
    # primary key
    id: str

    # имя группы, используется в перечислении в User
    name: str
    
    # group properties
    desc: str
    policy: str

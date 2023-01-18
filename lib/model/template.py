import uuid

from pydantic import BaseModel


class Template(BaseModel):
    # primary key
    id: uuid.UUID

    # identifier used in AdminGUI to list all templates
    name: str

    # template message content
    head: str
    body: str
    
    # parameters could be enterred in GUI and later replaced by engine
    # add allowed arguments that is used by managers in template body
    username: str
    useremail: str
    usertimezone: str

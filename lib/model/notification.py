import uuid

from typing import List

from pydantic import BaseModel

from lib.model.template import Template

class Notification(BaseModel):
    # primary key
    id: uuid.UUID

    # identifier used in AdminGUI to list all templates
    name: str
    
    # notification type identificator
    type: str
    
    # user groups to send notification to
    groups: List[str]

    # template message content
    template_id: Template.id

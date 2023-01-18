import uuid

from abc import ABC, abstractmethod

from lib.model.template import Template


class ITemplate(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def get_template(self, name: str) -> Template:
        pass
    
    @abstractmethod
    def render_template(self, template: Template, context: dict) -> str:
        pass

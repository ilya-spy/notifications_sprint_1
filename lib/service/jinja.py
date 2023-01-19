# служба формирования запросов на выборку для подготовки рассылок и анализа данных
# каждый воркер умеет запускать службу фоном для финалиной персонализации отправлений
from functools import lru_cache
from jinja2 import Template, Environment

from lib.model.template import Template as TemplateModel

from lib.api.v1.generator.template import ITemplate

class JinjaService():
    '''Template engine adapter class'''
    def __init__(self) -> ITemplate:
        self.environment = Environment()

        self.note_from_admin: str = \
        '''
            <html>
                <body>
                    <h4>Hello, {{ username }}</h4>
                    <p>Administrator is trying to reach you:</p>
                    <p>{{ body }}</p>
                </body>
            </html>
        '''
        self.weekly_releases: str = \
        '''
            <html>
                <body>
                    <h4>Hello, {{ username }}</h4>
                    <p>Weekly new releases for you:</p>
                    <p>{{ films_data }}</p>
                </body>
            </html>
        '''
        self.note_reaction: str = \
        '''
            <html>
                <body>
                    <h4>Hello, {{ username }}</h4>
                    <p>Recent events with your content:</p>
                    <p>{{ film_id }}</p>
                    <p>{{ film_name }} - {{ event_type }}</p>
                </body>
            </html>
        '''

    def render_template(self, template: Template, context: dict = {}):
        return template.render(**context)

    def get_template(self, template_name: TemplateModel.name) -> Template:
        template: Template = None

        if template_name == 'admin':
            template = self.environment.from_string(self.note_from_admin)

        if template_name == 'releases':
            template = self.environment.from_string(self.weekly_releases)

        if template_name == 'reaction':
            template = self.environment.from_string(self.note_reaction)

        return template


@lru_cache()
def get_templates() -> ITemplate:
    return JinjaService()

# служба формирования запросов на выборку для подготовки рассылок и анализа данных
# каждый воркер умеет запускать службу фоном для финалиной персонализации отправлений
from jinja2 import Template

from lib.db.models.template import Template as TemplateDB
from lib.db.models.user import User as UserDB

from core.get_user import ApiUserInfoAbstract

class EnrichService():
    '''Personalize context and render final message before sending'''

    def __init__(
        self,
        userapi: ApiUserInfoAbstract,
    ) -> None:
        pass

    @staticmethod
    def render_template(template, context=None):
        if not context:
            context = {}
        template = Template(template)
        return template.render(context)

    def get_template(template_id: TemplateDB.id):
        template_raw = self.db.get_template(message_rabbit.template_id)

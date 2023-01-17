# служба формирования запросов на выборку для подготовки рассылок и анализа данных
# каждый воркер умеет запускать службу фоном для финалиной персонализации отправлений
from jinja2 import Template

from lib.model.template import Template as TemplateModel

from lib.api.v1.admin.notification import INotification
from lib.api.v1.generator.template import ITemplate

class EnrichService():
    '''Personalize context and render final message before sending'''
    def __init__(
            self,
            itemplate: ITemplate,
            inotification: INotification
    ):
        self.templater = itemplate
        self.notifier = inotification

    @staticmethod
    def render_template(model: TemplateModel, context=None):
        if not context:
            context = {}
        template = Template(model.body)
        return template.render(context)

    def get_template(self, template_id: TemplateModel.id):
        return self.templater.get_template(template_id)

    def render_personalized(self, model: TemplateModel, context=dict, params=dict()):
        # override default userinfo from admin
        context.update(params)
        return self.render_template(model, context)

# служба формирования запросов на выборку для подготовки рассылок и анализа данных
# каждый воркер умеет запускать службу фоном для финалиной персонализации отправлений

from lib.model.template import Template as TemplateModel

from lib.api.v1.admin.notification import INotification
from lib.api.v1.generator.template import ITemplate

from lib.service.jinja import Template, get_templates


class EnrichService():
    '''Personalize context and render final message before sending'''
    def __init__(
            self,
            itemplate: ITemplate,
            inotification: INotification
    ):
        self.templater: ITemplate = itemplate
        self.notifier = inotification


    def get_template(self, template_name: TemplateModel.name):
        return self.templater.get_template(template_name)

    def render_personalized(self, template: Template, context=dict, params=dict()):
        # override default userinfo from admin
        context.update(params)
        return self.templater.render_template(template, context)


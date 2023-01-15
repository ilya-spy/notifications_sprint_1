from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class Person(UUIDMixin, TimeStampedMixin, models.Model):
    full_name = models.CharField(_("full_name"), max_length=255)
    birth_date = models.DateField(blank=False, null=True)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("person")

    def __str__(self):
        return self.full_name

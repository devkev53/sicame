from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Income(models.Model):
    date = models.DateField(_('date'), help_text=_('Automatic date at creation time'))
    time = models.TimeField(_('time'), help_text=_('Automatic time at creation time'))
    reference = models.CharField(_('Reference'), help_text=_('Document number as purchase or donation reference'))
    state = models.BooleanField(_('Available'), default=False)
    description = models.TextField(_('Description'), default='S/D', max_length=100)

    class Meta:
        verbose_name = _("Income")
        verbose_name_plural = _("Incomes")

    def __str__(self):
        return self.name

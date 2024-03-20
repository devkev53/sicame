from django.db import models
from django.utils.translation import gettext as _
from registration.models import User
from datetime import date
from crum import get_current_user


# Create your models here.

class BaseModel(models.Model):
    """Model definition for BaseModel."""

    # TODO: Define fields here
    created_by = models.ForeignKey(
        User, verbose_name=_('Created by'),
        on_delete=models.CASCADE,
        related_name='created_by%(app_label)s_%(class)s_related',
        blank=True, null=True, editable=False)
    created = models.DateField(
        _('Created'), auto_now_add=True, blank=True, null=True)
    updated_by = models.ForeignKey(
        User, verbose_name=_('Updated by'),
        on_delete=models.CASCADE,
        related_name='updated_by%(app_label)s_%(class)s_related',
        blank=True, null=True, editable=False)
    updated = models.DateField(
        _('Updated'), auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        """Meta definition for BaseModel."""
        abstract = True
        verbose_name = "Base"
        verbose_name_plural = "Bases"

    def __str__(self):
        """Unicode representation of BaseModel."""
        pass

    def save(self, *args, **kwargs):
        """Save method for BaseModel."""
        # Guardando el user
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.created_by = user
            else:
                self.userUpdate = user
        super(BaseModel, self).save()
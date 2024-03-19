from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from crum import get_current_user

# Create your models here.

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', blank=True, null=True, default=None, editable=False)
    modified = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_by', blank=True, null=True, default=None, editable=False)

    class Meta:
        verbose_name = _("BaseModel")
        verbose_name_plural = _("BaseModels")

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(BaseModel, self).save(*args, **kwargs)
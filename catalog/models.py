from django.db import models
from django.utils.translation import gettext as _
from core.models import BaseModel
from core.utils import drawImg

# Create your models here.

class Brand(BaseModel):
    name = models.CharField(_('Brand'), max_length=100)
    img = models.ImageField(_('image'), blank=True, null=True, upload_to='brand/')

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def showImg(self):
        return drawImg(self.name, self.img)
    showImg.short_description = _('Show Img')



class Category(BaseModel):
    name = models.CharField(_('Category'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name


class BaseObject(BaseModel):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'))
    img = models.ImageField(_('image'))


    class Meta:
        verbose_name = _("BaseObject")
        verbose_name_plural = _("BaseObjects")
        abstract = True

    def __str__(self):
        return self.name

    def stock(self):
        total = 0
        return total


class Material(BaseObject):


    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name


class Equipment(BaseObject):


    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipments")

    def __str__(self):
        return self.name


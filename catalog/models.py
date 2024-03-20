from django.db import models
from django.urls import reverse
from core.models import BaseModel
from django.utils.translation import gettext as _
from core.utils import preview_img

# Create your models here.

class Category(BaseModel):
    name = models.CharField(_('name'), max_length=100)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Brand(BaseModel):
    name = models.CharField(_('name'), max_length=75)
    logo_img = models.ImageField(_('logo image'), upload_to='brand/logo', blank=True, null=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})

    def preview_img(self):
        return preview_img(self.name, self.logo_img)


class ObjectBase(BaseModel):
    ''' Model for creation of object base '''
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('Description'), default='S/D')
    id_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"), blank=True, null=True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Brand"), blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to=('catalogo/imgs/'), blank=True, null=True)
    state = models.BooleanField(_('Available'), default=False)


    class Meta:
        abstract = True
        verbose_name = _("ObjectBase")
        verbose_name_plural = _("ObjectBases")

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.upper()

    def get_absolute_url(self):
        return reverse("ObjectBase_detail", kwargs={"pk": self.pk})


class Material(ObjectBase):


    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})

    def preview_image(self):
        return preview_img(self.name, self.image)

    def stock(self):
        return 0

    def assigned(self):
        return 0

    def turned(self):
        return 0

    def consumed(self):
        return 0

    def in_warehouse(self):
        return 0


class Equipment(ObjectBase):

    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Equipment_detail", kwargs={"pk": self.pk})

    def stock(self):
        return 0

    def preview_image(self):
        return preview_img(self.name, self.image)
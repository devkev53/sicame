from django.db import models
from core.models import BaseModel
from catalog.models import Material
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.


class EntryMaterial(BaseModel):
    reference = models.CharField(_('Reference'), help_text=_('''
        Field for the Document No. that will
        serve as a reference for the purchase
        or donation
    '''), max_length=250)
    state = models.BooleanField(_('Available'), default=False)
    description = models.TextField(_('Description'), default='S/D')


    class Meta:
        verbose_name = _("EntryMaterial")
        verbose_name_plural = _("Entries Materials")

    def __str__(self):
        return "%s %s" % (self.self.reference)

    def get_absolute_url(self):
        return reverse("Entries_detail", kwargs={"pk": self.pk})

    def total(self):
        return 0.00


class DetailBase(BaseModel):
    quantity = models.PositiveSmallIntegerField(_('Quantity'), default=1)
    id_entry = models.ForeignKey(EntryMaterial, on_delete=models.CASCADE)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2, default=0.00)
    location = models.CharField(_('Location'), max_length=250, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _("DetailBase")
        verbose_name_plural = _("DetailBases")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DetailBase_detail", kwargs={"pk": self.pk})


class MaterialEntryDetail(DetailBase):
    id_material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name=_('Material'))

    class Meta:
        verbose_name = _("MaterialEntryDetail")
        verbose_name_plural = _("MaterialEntryDetails")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MaterialEntryDetail_detail", kwargs={"pk": self.pk})





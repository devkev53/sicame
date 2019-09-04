from django.db import models
from core.models import BaseObjeto

''' * Importacion que nos permite maquetar o formatear
con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

''' * Importamos el MODELS para trabajar con el PERFIL * '''
from registration.models import Perfil

# Create your models here.


class Material(BaseObjeto):

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def image_thub(self):
        if self.img_thubmnail:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=self.img_thubmnail.url,
                width=50,
                height=50,
                ))
        else:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url='/../static/core/img/no-img.jpg',
                width=50,
                height=50,
                ))
    image_thub.short_description = 'Imagen'

    def stock(self):
        total = 'Muestra el Total'
        return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    stock.short_description = 'Registrado'

    def disponible(self):
        total = 'Muestra el Disponible'
        return format_html(
                '<span style="color: #009A19; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    disponible.short_description = 'Disponible'

    def asignado(self):
        total = 'Asginado'
        return format_html(
                '<span style="color: #265787; font-weight: bold; text-shadow: 0px 0px 2px #A1E8FD;">' +
                str(total) + '</span>')
    asignado.short_description = 'Asignado'

    def transformado(self):
        total = 'Transformado'
        return format_html(
                '<span style="color: #D17B00; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    transformado.short_description = 'Transformado'

    def monto_bodega(slef):
        total = 'Transformado'
        return format_html(
                '<span style="color: #616669; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    monto_bodega.short_description = 'Monto Total'

    def __str__(self):
        return '%s %s' % (self.nombre, self.id_Marca)


class Ingreso(models.Model):
    fecha = models.DateField(
        'Fecha', auto_now_add=True, help_text='Se tomara la fecha automatica de creacion')
    hora = models.TimeField(
        'Hora', auto_now_add=True, help_text='Se tomara la fecha automatica de creacion')
    referencia = models.CharField(
        'No. de Referencia', max_length=75, help_text='Indique el No. de Documento que servira como ' +
        'referencia en la compra o donacion del material que ingresara a Bodega..!')
    disponible = models.BooleanField('Dispobible', default=False)

    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        verbose_name='Creado Por')

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        pass

from django.db import models

''' * Importacion que nos permite maquetar o formatear
con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

''' * Importamos el MODELS para trabajar con el PERFIL * '''
from registration.models import Perfil

# Create your models here.


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
        return self.referencia

from django.db import models

# Importaciones para trabajar con Signals
from django.dispatch import receiver
from django.db.models.signals import post_save

# Importacion que nos permite maquetar o formatear
# con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

# Importamos el MODELS para trabajar con el PERFIL * '''
from registration.models import Perfil

# Importamos el MODELS para trabajar con el PERFIL * '''
from catalogo.models import Material

# Create your models here.


# Creacion del Modelo Ingreso
class Ingreso(models.Model):
    fecha = models.DateField(
        'Fecha', auto_now_add=True, help_text='Se tomara la fecha automatica de creacion')
    hora = models.TimeField(
        'Hora', auto_now_add=True, help_text='Se tomara la fecha automatica de creacion')
    referencia = models.CharField(
        'No. de Referencia', max_length=75, help_text='Indique el No. de Documento que servira como ' +
        'referencia en la compra o donacion del material que ingresara a Bodega..!')
    estado = models.BooleanField('Disponible', default=False)

    # asingado = models.ForeignKey(
    #     Perfil, on_delete=models.CASCADE,
    #     verbose_name='Asignado a')

    # Campo que servira para saber quien realizo el ingreso
    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        verbose_name='Creado Por')

    # Metodo que mostrara los precios por unidad
    def ref(self):
        return 'No-%s' % (self.referencia)
    # Agrega una descripcion al metodo para mostrar en el Admin
    ref.short_description = 'Referencia'

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return self.referencia


# Creacion del Modelo Abstracto Base_Detalle
# Con el cual se manejaran el detalle de Materiales y Equipos
class Base_Detalle(models.Model):
    cantidad = models.PositiveIntegerField('Cantidad')
    id_ingreso = models.ForeignKey(
        Ingreso, on_delete=models.CASCADE,
        verbose_name='Ingreso')
    monto = models.DecimalField(
        'Monto', max_digits=12, decimal_places=2)
    cantidad = models.PositiveIntegerField(
        'Cantidad', default=1)
    ubicacion = models.CharField(
        'Ubicacion', max_length=75,
        help_text='Debo de corregir y anclar bien la ubicacion')
    ref_ingreso = models.CharField(
        'Ref.', max_length=75,
        help_text='Referencia segun el ingreso', editable=False)

    # Metodo que mostrara los precios por unidad
    def por_unidad(self):
        pu = self.monto/self.cantidad
        return pu
    # Agrega una descripcion al metodo para mostrar en el Admin
    por_unidad.short_description = 'Precio Unidad'

    # Metodo que mostrara los precios por unidad
    def fecha_ingreso(self):
        ingreso = Ingreso.objects.filter(id=self.id_ingreso.id).get()
        fecha = ingreso.fecha
        return fecha
    # Agrega una descripcion al metodo para mostrar en el Admin
    fecha_ingreso.short_description = 'Fecha Ingreso'

    class Meta:
        abstract = True
        verbose_name = "Base_Detalle"
        verbose_name_plural = "Base_Detalles"

    def __str__(self):
        return self.ref_ingreso


# Creacion de la Clase Material_Detalle
# La cual manejara el detalle del Ingreso
class Material_Detalle(Base_Detalle):
    id_material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        verbose_name='Material')

    # Metodo para crear una referencia de detalles
    # Segun la referencia padre de Ingreso
    def ref_m(self):
        ingreso = Ingreso.objects.filter(id=self.id_ingreso.id).get()
        ref = 'No-%s-%s' % (ingreso.referencia, self.id)
        self.ref_ingreso = ref
        return ref
    # Agrega una descripcion al metodo para mostrar en el Admin
    ref_m.short_description = 'Referencia'

    class Meta:
        verbose_name = "Detalle de Material"
        verbose_name_plural = "Detalle de Materiales"

    def __str__(self):
        return self.ref_m()


class Asignacion(Ingreso):

    class Meta:
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return '%s' % (self.create_by)

from django.db import models

from django.shortcuts import redirect

# Importamos para realizar un signal
from django.db.models.signals import post_save
from django.dispatch import receiver

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
from django.contrib.auth.models import User

# Importamos el MODELS para trabajar con el PERFIL * '''
from catalogo.models import Material

# Importamos la exepcion para mostrar el mensage de erro de validacion
from django.core.exceptions import ValidationError

# Importamos la libreria para random
import random

# Importamos el app de CK Editor para enriqueze la descripcion
from ckeditor.fields import RichTextField

# Create your models here.


# Creacion del Modelo Ingreso
class Ingreso(models.Model):
    fecha = models.DateField(
        'Fecha', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    hora = models.TimeField(
        'Hora', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    referencia = models.CharField(
        'Dato o No. de Referencia', max_length=75,
        help_text='Indique el No. de Documento que servira como ' +
        'Referencia en la compra, donacion o ingreso del material' +
        'Bodega de Electricidad..!')
    estado = models.BooleanField('Disponible', default=False)
    descripcion = models.CharField(
        'Descripcion', default='S/D', max_length=100,
        help_text='Descripcion del Ingreso o la Referencia de INgreso')

    # asingado = models.ForeignKey(
    #     Perfil, on_delete=models.CASCADE,
    #     verbose_name='Asignado a')

    # Campo que servira para saber quien realizo el ingreso
    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        verbose_name='Creado Por')

    def boleta(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Ingreso_PDF/?id=%s"'
            'target="_blank">'
            '<span class="icon-clipboard-list" align="center"></span></a>'
            % self.id)
    boleta.short_description = 'Detalle de Ingreso'

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

    def save(self):
        print('Se creo un nuevo ingreso')
        super(Ingreso, self).save()
        return redirect('ingerso_pdf', self.boleta())


# @receiver(post_save, sender=Ingreso)
# def post_save_detalleproducto(sender, instance, **kwargs):
#     # Verifico que se crea un detalleproducto
#     ingreso = Ingreso.objects.filter(id=instance.id).get()
#     if kwargs['created']:
#         ingreso.boleta()


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
        try:
            pu = self.monto/self.cantidad
            return pu
        except:
            return None
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

    def saldo_cantidad(self):
        ''' --- Metodo que sumara las cantidades ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        cantidad_saldo = self.cantidad
        # Creamos un query ordenado por fechas de los objetos
        # que tienen realcion con el material en cuestion
        detalles = Material_Detalle.objects.filter(
                    id_material=self.id_material).order_by(
                    'id_ingreso__fecha')
        # Recorremos el query par ir sumando
        for detalles in detalles:
            # Evaluamos si el primer dato es menor a la fecha acutal
            if detalles.id_ingreso.fecha < self.id_ingreso.fecha:
                # Si este es Menor hacemos la suma
                cantidad_saldo = cantidad_saldo + detalles.cantidad
        # Ahora creamos un QuerySet par verificar Devoluciones y que se resten
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id_material):
                    if detalle.id_devolucion.fecha <= self.id_ingreso.fecha:
                        cantidad_saldo = cantidad_saldo - detalle.desechados
        return cantidad_saldo

    def saldo_valores(self):
        ''' --- Metodo que sumara los valores ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        monto_saldo = self.monto
        # Creamos un query ordenado por fechas de los objetos
        # que tienen realcion con el material en cuestion
        detalles = Material_Detalle.objects.filter(
                    id_material=self.id_material).order_by(
                    'id_ingreso__fecha')
        # Recorremos el query par ir sumando
        for detalles in detalles:
            # Evaluamos si el primer dato es menor a la fecha acutal
            if detalles.id_ingreso.fecha < self.id_ingreso.fecha:
                # Si este es Menor hacemos la suma
                monto_saldo = monto_saldo + detalles.monto
        return monto_saldo

    def valor_promedio_ponderado(self):
        promedio = 0.00
        promedio = self.saldo_valores() / self.saldo_cantidad()
        return promedio
    valor_promedio_ponderado.short_description='P.P.P.'

    def estado(self):
        estado = self.id_ingreso.estado
        return estado

    class Meta:
        verbose_name = "Detalle de Material"
        verbose_name_plural = "Detalle de Materiales"
        ordering = ['id_ingreso__fecha']

    def __str__(self):
        return self.ref_m()

    def save(self):
        self.valor_promedio_ponderado()
        super(Material_Detalle, self).save()

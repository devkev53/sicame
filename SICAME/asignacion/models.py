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
from django.contrib.auth.models import User

# Importamos el MODELS para trabajar con el PERFIL * '''
from catalogo.models import Material

# Importamos la libreria para random
import random

# Create your models here.


class Asignacion(models.Model):
    asig_id = models.CharField(
        'Dato o No. de Referencia', max_length=15,
        help_text='Se asignara el numero de referencia',
        primary_key=True, unique=True,)
    fecha = models.DateField(
        'Fecha', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    hora = models.TimeField(
        'Hora', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    module = models.CharField('Modulo', max_length=50)
    estado = models.BooleanField('Estado', default=False)

    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Create',
        verbose_name='Creado Por')

    assigned_to = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Send',
        verbose_name='Asignado a')

    def get_rand_string(self):
        """Devuelve un string de 4 caracteres aleatorios"""
        return 'ASIG' + ''.join(random.choice(
            '0123456789') for i in
            range(10))

    def set_referncia(self):
        self.asig_id = self.get_rand_string().upper()
        return self.asig_id

    def estado_color(self):
        if self.estado is True:
            return format_html(
                '<span style="color: #009A19;' +
                'font-weight: bold; text-shadow: 0px 0px 2px #8AFF00;">' +
                'Aceptada' + '</span>')
        else:
            return format_html(
                '<span style="color: #D17B00; font-weight:' +
                ' bold; text-shadow: 0px 0px 2px yellow;">' +
                'Pendiente' + '</span>')
    estado_color.short_description = 'Estado'

    class Meta:
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return 'Creado por: %s, Asigando a: %s' % (
            self.create_by, self.assigned_to)

    def save(self):
        self.set_referncia()
        super(Asignacion, self).save()


class Material_Asig(models.Model):
    cantidad = models.PositiveIntegerField('Cantidad')
    id_asig = models.ForeignKey(
        Asignacion, on_delete=models.CASCADE,
        verbose_name='No. de Asignacion')
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
    id_material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        verbose_name='Material')

    # Metodo que mostrara los precios por unidad
    def por_unidad(self):
        pu = self.monto/self.cantidad
        return pu
    # Agrega una descripcion al metodo para mostrar en el Admin
    por_unidad.short_description = 'Precio Unidad'

    # Metodo que mostrara los precios por unidad
    def fecha_ingreso(self):
        asignacion = Asignacion.objects.filter(id=self.id_asig.id).get()
        fecha = asignacion.fecha
        return fecha
    # Agrega una descripcion al metodo para mostrar en el Admin
    fecha_ingreso.short_description = 'Fecha Ingreso'

    def ref_m(self):
        asignacion = Asignacion.objects.filter(id=self.id_asig.id).get()
        ref = 'No-%s-%s' % (asignacion.asig_id, self.id)
        self.ref_ingreso = ref
        return ref
    # Agrega una descripcion al metodo para mostrar en el Admin
    ref_m.short_description = 'Referencia'

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def __str__(self):
        return self.ref_ingreso

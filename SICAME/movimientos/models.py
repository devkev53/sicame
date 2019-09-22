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

from inventario.models import Material_Detalle

# Importamos el MODELS para trabajar con el PERFIL * '''
from catalogo.models import Material

# Importamos la libreria para random
import random

# Importamos la exepcion para mostrar el mensage de erro de validacion
from django.core.exceptions import ValidationError

# Create your models here.


def get_rand_string():
    """Devuelve un string de 10 caracteres aleatorios"""
    return 'ASIG' + ''.join(random.choice(
            '0123456789') for i in
            range(10))


def get_rand_string_dev():
    """Devuelve un string de 10 caracteres aleatorios"""
    return 'DEV' + ''.join(random.choice(
            '0123456789') for i in
            range(10))

# Inicio de la Clase Asignacion para asignar el material al Instructor


class Asignacion(models.Model):
    id_no = models.CharField(
        'Dato o No. de Referencia', max_length=15,
        help_text='Se asignara automaticamente un ID',
        primary_key=True, unique=True, default=get_rand_string)
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

    def set_referncia(self):
        self.id_no = self.id_no
        return self.id_no

    def monto_total(self):
        total = 0
        for material in Material_Asignado.objects.filter(
                id_asignacion=self.id_no):
            total = total+material.monto
        return total

    def estado_color(self):
        if self.estado is True:
            return format_html(
                '<span aling="center" class="icon-check-square-o" style="color: #009A19;' +
                'font-weight: bold; font-size:22px; text-shadow: 0px 0px 2px #8AFF00;">' +
                '</span>')
        else:
            return format_html(
                '<span aling="center" class="icon-share-square-o" style="color: #D17B00;' +
                'font-weight: bold; font-size:22px; text-shadow: 0px 0px 2px yellow;">' +
                '</span>')
    estado_color.short_description = 'Estado'

    def detalle(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Detalle/?id=%s"'
            'target="_blank">'
            '<span class="icon-printer6" align="center"></span></a>'
            % self.id_no)
    detalle.short_description = 'Detalle'

    class Meta:
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return '%s, Fecha: %s, Modulo: %s' % (
            self.id_no, self.fecha, self.module)

    def save(self):
        self.set_referncia()
        super(Asignacion, self).save()


class Material_Asignado(models.Model):
    id_asignacion = models.ForeignKey(
        Asignacion, on_delete=models.CASCADE,
        verbose_name='Ingreso')
    cantidad = models.PositiveIntegerField(
        'Cantidad', default=1)
    ubicacion = models.CharField(
        'Ubicacion', max_length=75,
        help_text='Debo de corregir y anclar bien la ubicacion')
    monto = models.DecimalField(
        'Monto', max_digits=12, decimal_places=2, null=True)
    id_material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        verbose_name='Material')

    def img(self):
        img = self.id_material.img.url
        return img

    def fecha(self):
        asignacion = Asignacion.objects.filter(
            id_no=self.id_asignacion.id_no).get()
        return '%s' % (asignacion.fecha)

    def module(self):
        asignacion = Asignacion.objects.filter(
            id_no=self.id_asignacion.id_no).get()
        return '%s' % (asignacion.module)

    def p_ubidad_ppp(self):
        material = Material_Detalle.objects.filter(
            id_material=self.id_material).last()
        return material.valor_promedio_ponderado()

    def monto_ppp(self):
        material = Material_Detalle.objects.filter(
            id_material=self.id_material).last()
        self.monto = self.cantidad * material.valor_promedio_ponderado()
        return self.monto

    def id_asig(self):
        asignacion = Asignacion.objects.filter(
            id_no=self.id_asignacion.id_no).get()
        return '%s-M%s' % (asignacion.id_no, self.id)

    def estado(self):
        estado = self.id_asig.estado
        return estado

    class Meta:
        verbose_name = "Material Asignado"
        verbose_name_plural = "Materiales Asignados"

    def __str__(self):
        return self.id_asig()

    def save(self):
        self.monto_ppp()
        super(Material_Asignado, self).save()

    ''' -- Modificamos el metodo CLEAN para evaluar si existe materia
    dispobible y si es correcta la cantidad en la ubicacion a seleccionar--'''
    def clean(self, **kwargs):
        super(Material_Asignado, self).clean()

        material = Material.objects.filter(id=self.id_material.id).get()

        if self.cantidad < material.disponible_int():
            pass
        else:
            raise ValidationError(
                        'No se cuenta con la cantidad seleccionada, ' +
                        'la cantidad actuald disponible es de: ' +
                        str(material.disponible_int()))


class Devolucion(models.Model):
    id_no = models.CharField(
        'Dato o No. de Referencia', max_length=15,
        help_text='Se asignara automaticamente un ID',
        primary_key=True, unique=True, default=get_rand_string_dev)
    fecha = models.DateField(
        'Fecha', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    hora = models.TimeField(
        'Hora', auto_now_add=True,
        help_text='Se tomara la fecha automatica de creacion')
    asig_id = models.ForeignKey(
        Asignacion, on_delete=models.CASCADE,
        verbose_name='Ref. Asignacion',
        help_text='La devolucion debe conicidir con una Asignacion')
    estado = models.BooleanField('Estado', default=False)

    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Create_Dev',
        verbose_name='Creado Por')

    assigned_to = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Send_Dev',
        verbose_name='Asignado a')

    def set_referncia(self):
        self.id_no = self.id_no
        return self.id_no

    def monto_total(self):
        total = 0
        for material in Material_Asignado.objects.filter(
                id_asignacion=self.id_no):
            total = total+material.monto
        return total

    def estado_color(self):
        if self.estado is True:
            return format_html(
                '<span aling="center" class="icon-check-square-o" style="color: #009A19;' +
                'font-weight: bold; font-size:22px; text-shadow: 0px 0px 2px #8AFF00;">' +
                '</span>')
        else:
            return format_html(
                '<span aling="center" class="icon-share-square-o" style="color: #D17B00;' +
                'font-weight: bold; font-size:22px; text-shadow: 0px 0px 2px yellow;">' +
                '</span>')
    estado_color.short_description = 'Estado'

    def detalle(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Detalle/?id=%s"'
            'target="_blank">'
            '<span class="icon-printer6" align="center"></span></a>'
            % self.id_no)
    detalle.short_description = 'Detalle'

    class Meta:
        verbose_name = "Devolucion"
        verbose_name_plural = "Devoluciones"

    def __str__(self):
        return 'Creado por: %s, Asigando a: %s' % (
            self.create_by, self.assigned_to)

    def save(self):
        self.set_referncia()
        super(Devolucion, self).save()

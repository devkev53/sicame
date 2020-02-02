from django.db import models

# Importamos la clase Marca de Core
from core.models import Marca

# Importamos los Regex y ValidatorError para poder
from django.core.validators import RegexValidator

# Importamos la exepcion
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import redirect

# Importamos para realizar un signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Importaciones para trabajar con Signals
from django import dispatch
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save

# Importacion que nos permite maquetar o formatear
# con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

# Importamos el MODELS para trabajar con el PERFIL * '''
from registration.models import Perfil
from django.contrib.auth.models import User

# Importamos el MODELS para trabajar con el PERFIL * '''
from catalogo.models import Material, Equipo

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
    is_baja = models.BooleanField(default=False)

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

    def monto_ingreso(self):
        monto = 0
        for material in Material_Detalle.objects.filter(id_ingreso=self.id):
            monto = monto + material.monto
        for equipo in Equipo_Ingreso.objects.filter(id_ingreso=self.id):
            monto = monto + equipo.monto
        return monto

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return self.referencia

    def save(self):
        print('Se creo un nuevo ingreso')
        self.boleta()
        super(Ingreso, self).save()


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
        'Ubicacion', max_length=75,)
    ref_ingreso = models.CharField(
        'Ref.', max_length=75,
        help_text='Referencia segun el ingreso', editable=False)

    # Metodo que mostrara los precios por unidad
    def por_unidad(self):
        '''Este metodo se encarga de realizar una division
        sobre la el monto y la cantidad para obtener el valor
        unitario de cada material'''
        try:
            '''ntentamos obtener el monto y la cantidad
            y realizamos la revision''' 
            pu = self.monto/self.cantidad
            return ("%.2f" % pu)
        except:
            # De lo contario no regresamos nada
            return None
    # Agrega una descripcion al metodo para mostrar en el Admin
    por_unidad.short_description = 'Precio Unidad'

    # Metodo que mostrara los precios por unidad
    def fecha_ingreso(self):
        '''Metodo que recoje la fecha de ingreso del modelo Ingreos'''
        # Obtenemos el modelo ingreso referente al detalle
        ingreso = Ingreso.objects.filter(id=self.id_ingreso.id).get()
        # Creamos la variable de fecha con el dato del Ingreso
        fecha = ingreso.fecha
        # Devolvemos la fecha para mostrarla en detalle
        return fecha
    # Agrega una descripcion al metodo para mostrar en el Admin
    fecha_ingreso.short_description = 'Fecha Ingreso'

    def monto_point(self):
        return ("%.2f" % self.monto)

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

    # Metodo para calcular el valor promedio ponderado
    def valor_promedio_ponderado(self):
        '''Este metodo permitira traer el valor promedio ponderado
        servira para llamar el ulimo detalle de maetrial y utilizrlo
        en el Kardex'''
        # Se crea una variable y se realiza la division para obtener eldato
        promedio = self.saldo_valores() / self.saldo_cantidad()
        # Se retorna el valor que se obtiene
        return promedio
    valor_promedio_ponderado.short_description = 'P.P.P.'

    def valor_promedio_ponderado_str(self):
        promedio = 0.00
        promedio = self.saldo_valores() / self.saldo_cantidad()
        return ("%.2f" % promedio)
    valor_promedio_ponderado_str.short_description = 'P.P.P.'

    # Definicion de variable estado
    def estado(self):
        '''Metodo que recoje la fecha de ingreso del modelo Ingreos'''
        # Obtenemos el modelo ingreso referente al detalle
        # Creamos la variable de estado con el dato del Ingreso
        estado = self.id_ingreso.estado
        # Devolvemos el estado para mostrarla en detalle
        return estado

    class Meta:
        verbose_name = "Detalle de Material"
        verbose_name_plural = "Detalle de Materiales"
        ordering = ['id_ingreso__fecha']

    def __str__(self):
        return self.ref_m()

    # Llamamos al metodo save para sobreescribirlo
    def save(self):
        '''Modificaion del metodo save predeterminado
        de los modelos de django'''
        # Se ejecuta este metodo antes de guardar la instancia
        self.valor_promedio_ponderado()
        # Modifica la Instancia actual antes de guardar en la base de datos
        super(Material_Detalle, self).save()


@receiver(post_save, sender=Ingreso)
def validad_dispobible_Devolucion(sender, instance, **kwargs):
    if instance.estado is True:
        for material in Material_Detalle.objects.filter(
                id_ingreso=instance):
            if material.id_material.disponible_int != 0:
                Material.objects.filter(
                    id=material.id_material.id).update(estado=True)
            else:
                Material_Detalle.objects.filter(
                    id=material.id).update(estado=False)


# Creamos el modelo de ingreso de equipo este debe ser un,
# Este sera distinto al material ya que cada equipo tiene un id
class Equipo_Ingreso(models.Model):
    id_equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE,
        verbose_name='Equipo')
    id_ingreso = models.ForeignKey(
        Ingreso, on_delete=models.CASCADE,
        verbose_name='Ingreso')
    ibe = models.CharField(
        'No. de Inventario IBE', max_length=15,
        help_text='El no de Inventario IBE debe'
        ' seguir el siguiente formato X-XXX-XXXXX',
        validators=[
            RegexValidator(
                regex=r'^[I][/-][0-9]{3}[/-][0-9]{5}$',
                message='El Formato debe coincidir',
            ),
        ])
    monto = models.DecimalField(
        'Precio Unidad', max_digits=12, decimal_places=1)
    ubicacion = models.CharField(
        'Ubicacion', max_length=75,)
    ref_ingreso = models.CharField(
        'Ref.', max_length=75,
        help_text='Referencia segun el ingreso', editable=False)
    id_Marca = models.ForeignKey(
        Marca, on_delete=models.CASCADE,
        verbose_name='Marca')
    modelo = models.CharField(
        'Modelo', max_length=25,
        blank=True)
    serie = models.CharField(
        'Serie', max_length=25,
        blank=True)

    def monto_point(self):
        return ("%.2f" % self.monto)

    def estado(self):
        estado = self.id_ingreso.estado
        return estado

    def ref_m(self):
        ingreso = Ingreso.objects.filter(id=self.id_ingreso.id).get()
        ref = 'No-%s-%s-E' % (ingreso.referencia, self.id)
        self.ref_ingreso = ref
        return ref

    def monto_color(self):
        total = self.monto
        total = ("%.2f" % total)
        return format_html(
                '<span style="font-weight: bold;">Q. ' +
                total + '</span>')
    monto_color.short_description = 'Precop'

    def saldo_cantidad(self):
        ''' --- Metodo que sumara las cantidades ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        cantidad_saldo = 1
        # Creamos un query ordenado por fechas de los objetos
        # que tienen realcion con el material en cuestion
        detalles = Equipo_Ingreso.objects.filter(
                    id_equipo=self.id_equipo).order_by(
                    'id_ingreso__fecha')
        # Recorremos el query par ir sumando
        for detalles in detalles:
            # Evaluamos si el primer dato es menor a la fecha acutal
            if detalles.id_ingreso.fecha < self.id_ingreso.fecha:
                # Si este es Menor hacemos la suma
                cantidad_saldo = cantidad_saldo + 1
        return cantidad_saldo

    def saldo_valores(self):
        ''' --- Metodo que sumara los valores ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        monto_saldo = self.monto
        return monto_saldo

    class Meta:
        verbose_name = "Detalle de Equipo"
        verbose_name_plural = "Detalle de Equipos"

    def __str__(self):
        return self.ibe

    def save(self):
        super(Equipo_Ingreso, self).save()

    def clean(self, **kwargs):
        super(Equipo_Ingreso, self).clean()


'''@receiver(post_save, sender=Equipo_Ingreso)
def ensure_profile_exits(sender, instance, **kwargs):
    detalle = Equipo_Ingreso.objects.filter(id=instance.id)
    ibe = None
    if kwargs.get('created', True):
        contador = 0
        for equipo in Equipo_Ingreso.objects.all():
            if equipo.categ == instance.categ:
                contador = contador + 1
            if equipo.id == instance.id:
                ibe = equipo.ibe
        if contador > 9:
            cadena = '000%s' % (str(contador))
            print('Se creo un nuevo objeto su id es: ' + str(contador))
            print('Su cadena es: ' + cadena)
            detalle.update(orden=cadena, ibe=(ibe+cadena))
        elif contador > 99:
            cadena = '00%s' % (str(contador))
            print('Se creo un nuevo objeto su id es: ' + str(contador))
            print('Su cadena es: ' + cadena)
            detalle.update(orden=cadena, ibe=(ibe+cadena))
        elif contador > 990:
            cadena = '0%s' % (str(contador))
            print('Se creo un nuevo objeto su id es: ' + str(contador))
            print('Su cadena es: ' + cadena)
            detalle.update(orden=cadena, ibe=(ibe+cadena))
        elif contador < 9:
            cadena = '0000%s' % (str(contador))
            print('Se creo un nuevo objeto su id es: ' + str(contador))
            print('Su cadena es: ' + cadena)
            detalle.update(orden=cadena, ibe=(ibe+cadena))'''


class Equipo_for_asig(Equipo_Ingreso):

    class Meta:
        proxy = True
        verbose_name = "Detalle de Equipo"
        verbose_name_plural = "Detalle de Equipos"

    def __str__(self):
        return '%s %s' % (self.ibe, self.id_equipo)

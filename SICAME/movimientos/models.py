from django.db import models
# Exepciones
from django.core.exceptions import ObjectDoesNotExist

# Importamos el app de CK Editor para enriqueze la descripcion
from ckeditor.fields import RichTextField

# Importamos los Regex y ValidatorError para poder
# validar el numero de telefono y que solo permita los
# datos validos * '''
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

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
from catalogo.models import Material, Equipo
from inventario.models import Equipo_Ingreso, Equipo_for_asig

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

    def asignado(self):
        name = self.assigned_to
        return format_html(
                '<span aling="center" style="font-weight: bold;">' +
                str(name) + '</span>')

    def devuelto(self):
        devuelto = False
        if Devolucion.objects.filter(asig_id=self.id_no).exists():
            devuelto = True
        return devuelto

    def set_referncia(self):
        self.id_no = self.id_no
        return self.id_no

    def monto_total(self):
        total = 0
        for material in Material_Asignado.objects.filter(
                id_asignacion=self.id_no):
            total = total+material.monto
        for equipo in Equipo_Asignado.objects.filter(
                id_asignacion=self.id_no):
            total = total+equipo.monto()
        return total

    def estado_asig_dev(self):
        dev_estado = ''
        if self.estado is True:
            if Devolucion.objects.filter(asig_id=self.id_no).exists():
                dev = Devolucion.objects.filter(asig_id=self.id_no).get()
                if dev.estado is True:
                    dev_estado = 'Dev_ok'
                else:
                    dev_estado = 'Dev_pend'
        return dev_estado

    def estado_color(self):
        dev_estado = ''
        rotate = 'none'
        if self.estado is True:
            if Devolucion.objects.filter(asig_id=self.id_no).exists():
                dev = Devolucion.objects.filter(asig_id=self.id_no).get()
                if dev.estado is True:
                    color1 = '#265787'
                    color2 = "yellow"
                    icono = 'icon-download8'
                    dev_estado = 'Dev_ok'
                else:
                    color1 = '#000'
                    color2 = "yellow"
                    icono = 'icon-back'
                    rotate = 'rotateY(180deg)'
                    dev_estado = 'Dev_pend'
            else:
                color1 = '#009A19'
                color2 = "#8AFF00"
                icono = 'icon-check-square-o'
            return format_html(
                '<span aling="center" class="' + icono + '"\
                style="\
                    color: ' + color1 + ';\
                    font-weight: bold;\
                    font-size:22px;\
                    text-shadow: 0px 0px 10px ' + color2 + ';\
                    transform:' + rotate + ';"></span>')
        else:
            return format_html(
                '<span aling="center" class="icon-share-square-o"\
                style="color: #D17B00;\
                font-weight: bold;\
                font-size:22px;\
                text-shadow: 0px 0px 10px yellow;>\
                transform:' + rotate + ';"></span>')
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
        ordering = ['-fecha', '-hora']
        verbose_name = "Asignacion"
        verbose_name_plural = "Asignaciones"

    def __str__(self):
        return '%s, Fecha: %s, Modulo: %s, Asignado: %s ' % (
            self.id_no, self.fecha, self.module, self.assigned_to)

    def save(self):
        self.set_referncia()
        super(Asignacion, self).save()


class Equipo_Asignado(models.Model):
    id_asignacion = models.ForeignKey(
        Asignacion, on_delete=models.CASCADE,
        verbose_name='Ingreso')
    id_equipo = models.ForeignKey(
        Equipo_for_asig, on_delete=models.CASCADE,
        verbose_name='Equipo')

    def ubicacion(self):
        equipo = Equipo_Ingreso.objects.filter(
            id=self.id_equipo.id).get()
        ubicacion = equipo.ubicacion
        return ubicacion

    def img(self):
        equipo = Equipo.objects.filter(
            id=self.id_equipo.id_equipo.id).get()
        img = equipo.img
        return img.url

    def estado(self):
        valor = self.id_asignacion.estado
        return valor

    def id_asig(self):
        asignacion = Asignacion.objects.filter(
            id_no=self.id_asignacion.id_no).get()
        return '%s-M%s' % (asignacion.id_no, self.id)

    def monto(self):
        total = self.id_equipo.monto
        return total

    def verificar_para_asignar(self):

        from inventario.models import Equipo_for_asig
        lista = []
        for ingresos in Equipo_for_asig.objects.filter(
                id_equipo=self.id_equipo.id_equipo):
            if ingresos.id_ingreso not in lista:
                lista.append(ingresos)
        count = len(lista)

        if count > 1:
            msg = ' ingresos pendientes de cambiar a \
            disponible que contienen este equipo'
        else:
            msg = ' ingreso pendiente de cambiar a \
            disponible que contienen este equipo'

        equipo = Equipo.objects.filter(
            id=self.id_equipo.id_equipo.id).get()
        if equipo.disponible() >= 1:
            for equipo in Equipo_Asignado.objects.all():
                if self.id_equipo == equipo.id_equipo:
                    for dev in Devolucion.objects.filter(
                               asig_id=equipo.id_asignacion.id_no,
                               estado=False):
                        raise ValidationError(
                                'Este equipo ya se encuentra asignado ' +
                                'el No. de Asignacion es el: ' +
                                str(equipo.id_asignacion.id_no) +
                                ', seleccione otro con distinto IBE')
                else:
                    pass
        else:
            raise ValidationError(format_html(
                '<span aling="center" class="icon-error"\
                style="padding-right: 5px;"></span><span>'
                'Verifique la cantida dispobible ' +
                'el actual disponible es de: ' +
                str(equipo.disponible()) + ', Actualemnte' +
                ' tiene un total de ' + str(count) + msg + '</span>'))

    class Meta:
        verbose_name = "Equipo_Asignado"
        verbose_name_plural = "Equipo_Asignados"

    def __str__(self):
        return self.id_asig()

    ''' -- Modificamos el metodo CLEAN para evaluar si existe materia
    dispobible y si es correcta la cantidad en la ubicacion a seleccionar--'''
    def clean(self, **kwargs):
        super(Equipo_Asignado, self).clean()
        self.verificar_para_asignar()


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

    def dev(self):
        dev = False
        if self.id_asignacion.devuelto() is True:
            dev = True
        return dev

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

    def verificar_cantidad(self):
        material = Material.objects.filter(id=self.id_material.id).get()

        if self.cantidad < (
            material.disponible_int() -
                material.asignado_flotante()):
            pass
        else:
            raise ValidationError(format_html(
                '<span aling="center" class="icon-error"\
                style="padding-right: 5px;"></span><span>\
                No se cuenta con la cantidad seleccionada, ' +
                'la cantidad actuald disponible es de: ' +
                str(
                    material.disponible_int() -
                    material.asignado_flotante()) +
                '. Existe un asignado ' +
                'pendiente de aceptar de: ' +
                str(material.asignado_flotante()) + '</span>'))

    ''' -- Modificamos el metodo CLEAN para evaluar si existe materia
    dispobible y si es correcta la cantidad en la ubicacion a seleccionar--'''
    def clean(self, **kwargs):
        super(Material_Asignado, self).clean()
        self.verificar_cantidad()


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
        help_text='La devolucion debe conicidir con una Asignacion asi'
        'como los elementos deben cuadrar', blank=False, null=False, default=1)
    estado = models.BooleanField('Estado', default=False)

    create_by = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Create_Dev',
        verbose_name='Creado Por')

    assigned_to = models.ForeignKey(
        Perfil, on_delete=models.CASCADE,
        related_name='User_Send_Dev',
        verbose_name='Asignado a',
        help_text='Se asignara automaticamente a un '
        ' usuario encargado de bodega',)

    comentario = RichTextField(
        'Comentario', default='S/C',
        help_text='Ingrese un comentario de porque la devolucion,'
        'y como fue que se utilizaron los materiales o equipos'
        'para enriquecer la informacion agregada')

    def set_referncia(self):
        self.id_no = self.id_no
        return self.id_no

    def monto_desecho(self):
        total = 0
        for material in Material_Devuelto.objects.filter(
                id_devolucion=self.id_no):
            total = total+material.saldo_desechados()
        return total
        for equipo in Equipo_Devuelto.objects.filter(
                id_devolucion=self.id_no):
            if equipo.estado == 'Mlo.':
                total = total + equipo.id_equipo.monto
        return total

    def monto_total(self):
        total = 0
        for material in Material_Devuelto.objects.filter(
                id_devolucion=self.id_no):
            total = total+material.monto()
        for equipo in Equipo_Devuelto.objects.filter(
                id_devolucion=self.id_no):
            total = total+equipo.monto()
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

    def detalle_dev(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Detalle_dev/?id=%s"'
            'target="_blank">'
            '<span class="icon-printer6" align="center"></span></a>'
            % self.id_no)
    detalle_dev.short_description = 'Detalle'

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = "Devolucion"
        verbose_name_plural = "Devoluciones"

    def __str__(self):
        return 'Creado por: %s, Asigando a: %s' % (
            self.create_by, self.assigned_to)

    def validation(self):
        pass

    def if_out(self):
        valor = False
        for material in Material_Devuelto.objects.filter(
                    id_devolucion=self.id_no):
            if material.desechados > 0:
                valor = True
        for equipo in Equipo_Devuelto.objects.filter(
                    id_devolucion=self.id_no):
            if equipo.estado == 'Mlo.':
                valor = True
        return valor

    def save(self):
        self.set_referncia()
        super(Devolucion, self).save()

    def clean(self, **kwargs):
        super(Devolucion, self).clean()
        self.validation()


class Material_Devuelto(models.Model):
    id_devolucion = models.ForeignKey(
        Devolucion, on_delete=models.CASCADE,
        verbose_name='Devolucion')
    buenos = models.PositiveIntegerField(
        'Sin Utilizar', default=0,
        help_text='Material que no se utilizo')
    transformados = models.PositiveIntegerField(
        'Trasformados o utilizados', default=0,
        help_text='Material que se utilizo para'
        ' practica o se convirtio en modelo didactico')
    desechados = models.PositiveIntegerField(
        'Desechados', default=0,
        help_text='Material que en practica fue dechado')
    total = models.PositiveIntegerField(
        'Total', default=0)


    def monto(self):
        total = self.total_sum() * self.valor_por_unidad()
        return total

    def total_sum(self):
        self.total = self.buenos + self.transformados + self.desechados
        return self.total

    id_material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        verbose_name='Material', blank=False, null=False)

    def saldo_desechados(self):
        sub = 0
        from inventario.models import Material_Detalle
        for ingreso_material in Material_Detalle.objects.filter(
                id_material=self.id_material):
            if ingreso_material.id_ingreso.fecha < self.id_devolucion.fecha:
                sub = (
                    self.desechados *
                    ingreso_material.valor_promedio_ponderado())
        return sub

    def valor_por_unidad(self):
        sub = 0
        from inventario.models import Material_Detalle
        for ingreso_material in Material_Detalle.objects.filter(
                id_material=self.id_material):
            if ingreso_material.id_ingreso.fecha < self.id_devolucion.fecha:
                sub = (
                    ingreso_material.valor_promedio_ponderado())
        return sub

    def saldo_cantidad(self):
        ''' --- Metodo que sumara las cantidades ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        cantidad_saldo = 0
        # Creamos un query ordenado por fechas de los objetos
        # que tienen realcion con el material en cuestion
        detalles = Material_Detalle.objects.filter(
                    id_material=self.id_material).order_by(
                    'id_ingreso__fecha')
        # Recorremos el query par ir sumando
        for detalles in detalles:
            # Evaluamos si el primer dato es menor a la fecha acutal
            if detalles.id_ingreso.fecha < self.id_devolucion.fecha:
                # Si este es Menor hacemos la suma
                cantidad_saldo = cantidad_saldo + detalles.cantidad
        # Ahora creamos un QuerySet par verificar Devoluciones y que se resten
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id_material):
                    if detalle.id_devolucion.fecha <= self.id_devolucion.fecha:
                        cantidad_saldo = cantidad_saldo - detalle.desechados
        return cantidad_saldo

    def saldo_valores(self):
        ''' --- Metodo que sumara los valores ingresados en los
        detalles segun la fecha de ingreso de menor a mayor --- '''
        monto_saldo = 0
        # Creamos un query ordenado por fechas de los objetos
        # que tienen realcion con el material en cuestion
        detalles = Material_Detalle.objects.filter(
                    id_material=self.id_material).order_by(
                    'id_ingreso__fecha')
        # Recorremos el query par ir sumando
        for detalles in detalles:
            # Evaluamos si el primer dato es menor a la fecha acutal
            if detalles.id_ingreso.fecha < self.id_devolucion.fecha:
                # Si este es Menor hacemos la suma
                monto_saldo = monto_saldo + detalles.monto
        monto_saldo = monto_saldo - (self.valor_por_unidad()*self.desechados)
        return monto_saldo

    def validation_material(self):
        try:
            asig_mat = Material_Asignado.objects.filter(
                id_asignacion=self.id_devolucion.asig_id,
                id_material=self.id_material).get()
            if asig_mat.cantidad != self.total_sum():
                raise ValidationError(
                    'Se debe cuadrar la cantidad toal de materiales'
                    ' con la cantidad que fue entregada en la Asignacion')
        except ObjectDoesNotExist:
            raise ValidationError(
                    'Verifique la Asignacion seleccionada ya que no '
                    'existe este Material en la misma, o en su defecto '
                    'verifique que se este regresando la totalidad de '
                    'Materiales Asignacion Selecciondad = ' +
                    str(self.id_devolucion.asig_id))

    def vpp(self):
        total = 0
        total = (self.saldo_valores() / self.saldo_cantidad())
        return total

    class Meta:
        verbose_name = "Material Devuelto"
        verbose_name_plural = "Materiales Devueltos"

    def __str__(self):
        return '%s' % (self.id_devolucion)

    def save(self):
        self.total_sum()
        super(Material_Devuelto, self).save()

    # Llamamos el memtodo clean para sobrescribir el mismo
    def clean(self, **kwargs):
        '''Obtiene los campos de formulario para ser evaluados
        o bien modificados, segun las isntrucciones que se asignen'''
        # Obtiene los datos del formualrio de la clase antes de guardar
        super(Material_Devuelto, self).clean()
        # Modifica el campo total
        self.total_sum()
        # Valida que se cuente con material para asignar
        self.validation_material()


ESTADOS_DEL_EQUIPO = [
    ('Bno.', 'Bueno'),
    ('Mlo.', 'Malo'),
    ('Rlr.', 'Con Daño'),
]


class Equipo_Devuelto(models.Model):
    id_devolucion = models.ForeignKey(
        Devolucion, on_delete=models.CASCADE,
        verbose_name='Devolucion')
    id_equipo = models.ForeignKey(
        Equipo_for_asig, on_delete=models.CASCADE,
        verbose_name='Equipo')
    estado = models.CharField(
        max_length=4,
        choices=ESTADOS_DEL_EQUIPO,
        default='Bueno',)
    comentarios = models.TextField('Comentarios')

    def img(self):
        equipo = Equipo.objects.filter(
            id=self.id_equipo.id_equipo.id).get()
        img = equipo.img
        return img.url

    def estado_dev(self):
        valor = self.id_devolucion.estado
        return valor

    def validation_material(self):
        try:
            asig_mat = Material_Asignado.objects.filter(
                id_asignacion=self.id_devolucion.asig_id,
                id_material=self.id_material).get()
            if asig_mat.cantidad != self.total_sum():
                raise ValidationError(
                    'Se debe cuadrar la cantidad toal de materiales'
                    ' con la cantidad que fue entregada en la Asignacion')
        except ObjectDoesNotExist:
            raise ValidationError(
                    'Verifique la Asignacion seleccionada ya que no '
                    'existe este Material en la misma, o en su defecto '
                    'verifique que se este regresando la totalidad de '
                    'Materiales Asignacion Selecciondad = ' +
                    str(self.id_devolucion.asig_id))

    def monto(self):
        total = self.id_equipo.monto
        return total

    class Meta:
        verbose_name = "Equipo Devuelto"
        verbose_name_plural = "Equipos Devueltos"

    def __str__(self):
        return '%s' % (self.id_devolucion)


class Recepccion(Devolucion):

    class Meta:
        proxy = True
        verbose_name = "Recepccion"
        verbose_name_plural = "Recepcciones"

    def __str__(self):
        return 'Creado por: %s, Asigando a: %s' % (
            self.create_by, self.assigned_to)

from django.db import models

# Importacion que nos permite maquetar o formatear
# con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Importamos los Regex y ValidatorError para poder
# validar el numero de telefono y que solo permita los
# datos validos * '''
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Importamos el MODELS para trabajar con el PERFIL
from django.contrib.auth.models import User

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

# Esta libreira es de pillow imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Importamos las librerias para usar senales
from django.dispatch import receiver
from django.db.models.signals import post_save

# Importacion de Material
from catalogo.models import Material

# Create your models here.


# Metodo que valida el Numero de Telefono
def val_tel(value):
    ''' Metodo que valida el numero de telefono y solo permite
    numeros, ademas no permite cadenas mayores a ocho numeros '''
    if not len(value) > 7:  # Si el largo es menor de 7
        raise ValidationError(  # Muesra un mensaje de error
            'Ingrese un numero de telefono valido')


# Metodo para eliminar una fotografia si ya existe
# en la base de datos y evitar llenar el especio '''
def custom_upload_to(instance, filename):
    ''' Metodo para borrar la imagen ya existente, en caso
    de acturalizar la imagen ya subida al sistema '''
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.foto.delete()
    return 'profile/' + filename


# Cracion de la Clase Perfil para manejo del Usuario
class Perfil(models.Model):
    ''' Declaracion de la Clase Perfil para controlar los perfiles
    de usuario, ingresados al sistema '''
    user = models.OneToOneField(
        User, verbose_name='Usuario', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    direccion = models.CharField('Direccion', max_length=50, blank=True)
    telefono = models.CharField(
            'Telefono', validators=[RegexValidator(
                regex=r'^[0-9]*$',
                message=('Ingrese solamente numeros'),
            ), val_tel], max_length=8, blank=True)
    is_instructor = models.BooleanField('Es Instructor', default=False)

    # Campo para crear una Thubmnail de la fotografia de perfil
    img_thubmnail = ImageSpecField(
        source='foto',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60})

    def image_thub(self):
        if self.img_thubmnail:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.img_thubmnail.url,
                    width=50,
                    height=50,
                ))
        else:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url='/../static/core/img/no-img.jpg',
                    width=50,
                    height=50,
                ))
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    image_thub.short_description = 'Avatar'

    # Metodo Para regresar el Nombre Completo
    def full_name(self):
        ''' Regresa el nombre completo del perfil '''
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return '%s' % (self.user)
    # Retorna una descripcion en el ADMIN del Metodo
    full_name.short_description = 'Nombre'

    def material_int(self):
        total = 0
        from movimientos.models import Material_Devuelto, Devolucion
        from movimientos.models import Asignacion, Material_Asignado
        for asignacion in Asignacion.objects.filter(
                assigned_to=self.id, estado=True):
            for material in Material_Asignado.objects.filter(
                    id_asignacion=asignacion):
                total = total + material.monto
            for devolucion in Devolucion.objects.filter(
                        create_by=self.id, estado=True,
                        asig_id=asignacion):
                for material in Material_Asignado.objects.filter(
                        id_asignacion=asignacion):
                    total = total - material.monto
        return total

    def material_asignado(self):
        total = self.material_int()
        t = ("%.2f" % total)
        return format_html(
                '<span style="color: #265787; font-weight: bold;' +
                'text-shadow: 0px 0px 2px #A1E8FD;">Q. ' +
                t + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    material_asignado.short_description = 'Q. Material'

    def equipo_int(self):
        total = 0
        from movimientos.models import Asignacion, Equipo_Asignado
        for asignacion in Asignacion.objects.filter(
                assigned_to=self.id, estado=True):
            for equipo in Equipo_Asignado.objects.filter(
                    id_asignacion=asignacion):
                total = total + equipo.monto()
        # Importamos el total de las devoluciones por perfil
            from movimientos.models import Devolucion, Equipo_Devuelto
            for devolucion in Devolucion.objects.filter(
                    create_by=self.id, estado=True, asig_id=asignacion):
                for e_dev in Equipo_Devuelto.objects.filter(
                        id_devolucion=devolucion, estado='Bno.'):
                    total = total - e_dev.monto()
        return total

    def equipo_asignado(self):
        total = self.equipo_int()
        t = ("%.2f" % total)
        return format_html(
                '<span style="color: #000; font-weight: bold;' +
                'text-shadow: 0px 0px 2px #616669;">Q. ' +
                t + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    equipo_asignado.short_description = 'Q. Equipo'

    def total_asignado(self):
        total = self.total_int()
        t = ("%.2f" % total)
        return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-decoration:underline;' +
                'text-shadow: 0px 0px 2px yellow;">Q. ' +
                t + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    total_asignado.short_description = 'Monto Q. Total'

    def total_int(self):
        total = self.equipo_int() + self.material_int()
        return total

    class Meta:
        verbose_name = "Perfile"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return '%s' % (self.full_name())

    def tarjeta(self):
            ''' Llama al un template que sera drenderizado como un pdf'''
            return mark_safe(
                u'<a class="print"'
                'href="/Tarjeta_de_Responsabilidad_PDF/?id=%s"'
                'target="_blank">'
                '<span><span class="icon-id-card-o" align="center"></span>'
                '<span class="icon-moneybag" align="center"></span></span></a>'
                % self.id)
    tarjeta.short_description = 'Tarjeta de Responsabilidad'


@receiver(post_save, sender=User)
def ensure_profile_exits(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)
        print('se acaba de crear un usuario y su perfil enlazado')


class Mi_Perfil(Perfil):

    class Meta:
        proxy = True
        verbose_name = "Mi Perfil"
        verbose_name_plural = "Mi Perfil"

    def __str__(self):
        return '%s' % (self.full_name())

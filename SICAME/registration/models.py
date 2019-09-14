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
def val_tel(value):  # Funcion no permite menos de 7 #
    if not len(value) > 7:  # Si el largo es menor de 7
        raise ValidationError(  # Muesra un mensaje de error
            'Ingrese un numero de telefono valido')


# Metodo para eliminar una fotografia si ya existe
# en la base de datos y evitar llenar el especio '''
def custom_upload_to(instance, filename):
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.foto.delete()
    return 'profile/' + filename


# Cracion de la Clase Perfil para manejo del Usuario
class Perfil(models.Model):
    user = models.OneToOneField(
        User, verbose_name='Usuario', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    direccion = models.CharField('Direccion', max_length=50, blank=True)
    telefono = models.CharField(
            'Telefono', validators=[RegexValidator(  # Clases para hacer validaciones
                regex=r'^[0-9]*$',  # cadenas permitidas
                message=('Ingrese solamente numeros'),  # Mensaje de error
            ), val_tel], max_length=8, blank=True)  # Caracteres maximos)
    puesto = models.CharField('Puesto', max_length=25, blank=True)

    # Campo para crear una Thubmnail de la fotografia de perfil
    img_thubmnail = ImageSpecField(
        source='foto',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60})

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
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    image_thub.short_description = 'Avatar'

    # Metodo Para regresar el Nombre Completo
    def full_name(self):
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return '%s' % (self.user)
    # Retorna una descripcion en el ADMIN del Metodo
    full_name.short_description = 'Nombre'

    def material_asignado(self):
        total = '0.00'
        return format_html(
                '<span style="color: #265787; font-weight: bold; text-shadow: 0px 0px 2px #A1E8FD;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    material_asignado.short_description = 'Q. Material'

    def equipo_asignado(self):
        total = '0.00'
        return format_html(
                '<span style="color: #000; font-weight: bold; text-shadow: 0px 0px 2px #616669;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    equipo_asignado.short_description = 'Q. Equipo'

    def Total_asignado(self):
        total = '0.00'
        return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    Total_asignado.short_description = 'Monto Q. Total'

    class Meta:
        verbose_name = "Perfile"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return '%s' % (self.full_name())


@receiver(post_save, sender=User)
def ensure_profile_exits(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)
        print('se acaba de crear un usuario y su perfil enlazado')


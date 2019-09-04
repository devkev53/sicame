from django.db import models
''' * Importamos los Regex y ValidatorError para poder
validar el numero de telefono y que solo permita los
datos validos * '''
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Importamos el MODELS para trabajar con el PERFIL
from django.contrib.auth.models import User

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

# Esta libreira es de pillow imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


def val_tel(value):  # Funcion no permite menos de 7 #
    if not len(value) > 7:  # Si el largo es menor de 7
        raise ValidationError(  # Muesra un mensaje de error
            'Ingrese un numero de telefono valido')


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.foto.delete()
    return 'profile/' + filename


class Profile(models.Model):
    user = models.OneToOneField(
        User, verbose_name='Usuario', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    direccion = models.CharField('Direccion', max_length=50)
    telefono = models.CharField(
            'Telefono', validators=[RegexValidator(  # Clases para hacer validaciones
                regex=r'^[0-9]*$',  # cadenas permitidas
                message=('Ingrese solamente numeros'),  # Mensaje de error
            ), val_tel], max_length=8)  # Caracteres maximos)
    puesto = models.CharField('Puesto', max_length=25)

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

    def full_name(self):
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user
    full_name.short_description = 'Nombre'

    class Meta:
        verbose_name = "Perfile"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return '%s' % (self.full_name())

from django.db import models
from core.models import *


''' * Importacion que nos permite maquetar o formatear
con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Importamos el app de CK Editor para enriqueze la descripcion
from ckeditor.fields import RichTextField

''' * Librerias de importacion de PILLOW para poder
mostrar thubnails de las imagenes subidas al sistema*'''
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Impotamos Mark_Safe para poder mostar la img en el Admin
from django.utils.safestring import mark_safe

# Create your models here.


# Metodo para eliminar una fotografia si ya existe
# en la base de datos y evitar llenar el especio '''
def custom_upload_to(instance, filename):
    old_instance = Material.objects.get(pk=instance.pk)
    old_instance.foto.delete()
    return 'Catalogo/Material' + filename


# Creacion del Modelo Abstracto BaseObjeto
class BaseObjeto(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = RichTextField('Descripcion', default='S/D')
    id_Marca = models.ForeignKey(
        Marca, verbose_name='Marca', on_delete=models.CASCADE)
    id_Categoria = models.ForeignKey(
        Categoria, verbose_name='Categoria', on_delete=models.CASCADE)
    img = models.ImageField(
        upload_to='Catalogo/', null=True, blank=True, verbose_name='Imagen')

    # campo que creara la imagen en thubnail
    img_thubmnail = ImageSpecField(
        source='img',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60})

    class Meta:
        abstract = True
        verbose_name = "BaseObjeto"
        verbose_name_plural = "BaseObjetos"

    def __str__(self):
        return '%s' % (self.nombre)


# Creacion del Modelo Material
class Material(BaseObjeto):

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    # Metodo que mostara la img thubnail si no la encutra mostara otra
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
    image_thub.short_description = 'Imagen'

    # Metodo que devolvera el stock de materiales ingresados en Bodega
    def stock(self):
        total = 0
        try:
            # Importamos las librerias de Inventario
            from inventario.models import Material_Detalle

            for detalle in Material_Detalle.objects.filter(
                    id_material=self.id):
                    total = total + detalle.cantidad
            return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')

        except Exception:
            return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
        else:
            return format_html(
                '<span style="color: #02AD02; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock.short_description = 'Registrado'

    # Metodo que devolvera el stock de materiales Disponibles
    def disponible(self):
        total = 'Muestra el Disponible'
        return format_html(
                '<span style="color: #009A19; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    disponible.short_description = 'Disponible'

    # Metodo que devolvera el stock de materiales Asignados
    def asignado(self):
        total = 'Asginado'
        return format_html(
                '<span style="color: #265787; font-weight: bold; text-shadow: 0px 0px 2px #A1E8FD;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    asignado.short_description = 'Asignado'

    # Metodo que devolvera el stock de materiales Transformados
    def transformado(self):
        total = 'Transformado'
        return format_html(
                '<span style="color: #D17B00; font-weight: bold; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    transformado.short_description = 'Transformado'

    # Metodo que devolvera el monto en quetzales del material en Bodega
    def monto_bodega(self):
        total = 0
        try:
            # Importamos las librerias de Inventario
            from inventario.models import Material_Detalle

            for detalle in Material_Detalle.objects.filter(
                    id_material=self.id):
                total = total + detalle.monto
            return format_html(
                '<span style="color: #616669; font-weight: bold; font-size: 18px; text-shadow: 0px 0px 2px yellow;">' +
                'Q. ' + str(total) + '</span>')

        except Exception:
            return format_html(
                '<span style="color: #616669; font-weight: bold; font-size: 18px; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
        else:
            return format_html(
                '<span style="color: #616669; font-weight: bold; font-size: 18px; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    monto_bodega.short_description = 'Monto Total'

    def __str__(self):
        return '%s, Marca: %s' % (self.nombre, self.id_Marca)

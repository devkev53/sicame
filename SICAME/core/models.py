from django.db import models

# Importamos el app de CK Editor para enriqueze la descripcion
from ckeditor.fields import RichTextField

''' * Librerias de importacion de PILLOW para poder
mostrar thubnails de las imagenes subidas al sistema*'''
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField('Nombre', max_length=100)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField('Nombre', max_length=100)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre


class BaseObjeto(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = RichTextField('Descripcion', default='S/D')
    id_Marca = models.ForeignKey(
        Marca, verbose_name='Marca', on_delete=models.CASCADE)
    id_Categoria = models.ForeignKey(
        Categoria, verbose_name='Categoria', on_delete=models.CASCADE)

    img = models.ImageField(
        upload_to='Catalogo/', null=True, blank=True, verbose_name='Imagen')

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


class Base_Detalle(models.Model):
    cantidad = models.PositiveIntegerField('Cantidad', default=1)

    class Meta:
        abstract = True
        verbose_name = "Base_Detalle"
        verbose_name_plural = "Base_Detalles"

    def __str__(self):
        pass

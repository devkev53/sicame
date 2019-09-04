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


class Base_Detalle(models.Model):
    cantidad = models.PositiveIntegerField('Cantidad', default=1)

    class Meta:
        abstract = True
        verbose_name = "Base_Detalle"
        verbose_name_plural = "Base_Detalles"

    def __str__(self):
        pass

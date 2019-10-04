from django.db import models
from core.models import *


''' * Importacion que nos permite maquetar o formatear
con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Importamos el app de CK Editor para enriqueze la descripcion
from ckeditor.fields import RichTextField

# Librerias de importacion de PILLOW para poder
# mostrar thubnails de las imagenes subidas al sistema*'''
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
        Marca, verbose_name='Marca', on_delete=models.CASCADE,
        blank=True)
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
        ordering = ['nombre']
        verbose_name = "Material o Insumo"
        verbose_name_plural = "Materiales o Insumos"

    # Permitira mostrar el Link de descarga del detalle del Ingreso
    def ficha(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Ficha_Kardex_PDF/?id=%s"'
            'target="_blank">'
            '<span class="icon-printer6" align="center"></span></a>'
            % self.id)
    ficha.short_description = 'T Kardex'

    # def listado(self):
    #     ''' Llama al un template que sera drenderizado como un pdf'''
    #     return mark_safe(
    #         u'<a class="print" href="/Listado_Material/?id=%s"'
    #         'target="_blank">'
    #         '<span class="icon-printer6" align="center"></span></a>'
    #         % self.id)
    # ficha.short_description = 'T Kardex'

    # Metodo que mostara la img thubnail si no la encutra mostara otra
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
    image_thub.short_description = 'Imagen'

    # Metodo que devolvera el stock de materiales ingresados en Bodega
    def stock(self):
        total = 0
        # Importamos las librerias de Inventario
        from inventario.models import Material_Detalle

        for detalle in Material_Detalle.objects.filter(
                id_material=self.id):
                total = total + detalle.cantidad
        if total == 0:
            total = '--'
        else:
            None
        return format_html(
            '<span style="color: #000;">' +
            str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock.short_description = 'Ingresado'

    # Metodo que devolvera el stock de materiales Disponibles
    def disponible_int(self):
        total = 0

        # Importamos las librerias de Inventario
        from inventario.models import Material_Detalle, Ingreso

        for ingreso in Ingreso.objects.filter(estado=True):
            for detalle in Material_Detalle.objects.filter(
                        id_material=self.id, id_ingreso=ingreso):
                        total = total + detalle.cantidad
        # Ahora Importamos las devoluciones para actulizar el disponible
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total - detalle.transformados - detalle.desechados
        total = total - self.asignado_int()
        return total

    # Metodo que devolvera el stock de materiales Disponibles
    def disponible(self):
        total = 0

        # Importamos las librerias de Inventario
        from inventario.models import Material_Detalle, Ingreso

        for ingreso in Ingreso.objects.filter(estado=True):
            for detalle in Material_Detalle.objects.filter(
                        id_material=self.id, id_ingreso=ingreso):
                        total = total + detalle.cantidad
        # Ahora Importamos las devoluciones para actulizar el disponible
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total - detalle.transformados - detalle.desechados

        # Ahora restamos el total asignado para no qeudarnos sin disponibles
        total = total - self.asignado_int()
        color1 = None
        color2 = None
        if total == 0:
            total = '--'
            color1 = '#D7142B'
            color2 = '#FF7800'
        else:
            if total <= 50:
                color1 = '#D7142B'
                color2 = "#FF7800"
            elif total <= 99:
                color1 = '#FF7800'
                color2 = 'yellow'
            else:
                color1 = '#009A19'
                color2 = '#8AFF00'

        return format_html(
                    '<span style="color:' + color1 + '; font-weight: bold;' +
                    ' text-shadow: 0px 0px 2px ' + color2 + ';">' +
                    str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    disponible.short_description = 'Disponible'

    # Metodo que devolvera el stock de materiales Asignados
    def asignado_int(self):
        total = 0
        from movimientos.models import Asignacion, Material_Asignado
        from movimientos.models import Devolucion, Material_Devuelto

        for asignacion in Asignacion.objects.filter(estado=True):
            for detalle in Material_Asignado.objects.filter(
                        id_material=self.id, id_asignacion=asignacion):
                        total = total + detalle.cantidad
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total - detalle.total_sum()
        return total

    # Metodo que devolvera el stock de materiales Asignados
    def asignado(self):
        total = 0
        from movimientos.models import Asignacion, Material_Asignado
        from movimientos.models import Devolucion, Material_Devuelto

        for asignacion in Asignacion.objects.filter(estado=True):
            for detalle in Material_Asignado.objects.filter(
                        id_material=self.id, id_asignacion=asignacion):
                        total = total + detalle.cantidad
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total - detalle.total_sum()
        if total == 0:
            total = '--'
        else:
            pass
        return format_html(
                '<span style="color: #265787; text-shadow: 0px 0px 2px #A1E8FD;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    asignado.short_description = 'Asignado'

    # Metodo que devolvera el stock de materiales Transformados
    def transformado(self):
        total = 0
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total + detalle.transformados
        if total == 0:
            total = '--'
        else:
            pass
        return format_html(
                '<span style="color: #520078; text-shadow: 0px 0px 2px yellow;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    transformado.short_description = 'Transformado'

    def consumido(self):
        total = 0
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                total = total + detalle.desechados
        if total == 0:
            total = '--'
        else:
            pass
        return format_html(
                '<span style="color: #000; text-shadow: 0px 0px 1px #919191;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    consumido.short_description = 'De Baja'

    def monto_bodega(self):
        total = 0
        sub = 0
        # Buscamos traer el total de consumidos
        consumido = 0
        from movimientos.models import Devolucion, Material_Devuelto
        for devolucion in Devolucion.objects.filter(estado=True):
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                    consumido = consumido + detalle.desechados
        # traemos el total ingresado a bodega
        bodega = 0
        from inventario.models import Material_Detalle
        for detalle in Material_Detalle.objects.filter(
                id_material=self.id):
                bodega = bodega + detalle.cantidad
        # Realizamos la resta del subtotal
        sub = bodega - consumido
        # Traemos el ultimo detalle de ingreso segun el material
        from inventario.models import Material_Detalle
        ultimo = Material_Detalle.objects.filter(
            id_material=self.id).last()
        # Recoremos los materiales para comparar con el ultimo
        for material in Material_Detalle.objects.all():
            if material == ultimo:
                total = sub * material.valor_promedio_ponderado()
        # Validamos que total no sea 0 para mostrar unicamente los 3 guines
        color = '#000'
        if total == 0:
            color = '#6B0000'
            total = '---'

        return format_html(
                '<span style="color: ' + color + '; font-weight: bold;">Q. ' +
                str(total) + '</span>')
    monto_bodega.short_description = 'Monto Total'

    def __str__(self):
        return '%s, Marca: %s' % (self.nombre, self.id_Marca)


class Equipo(BaseObjeto):

    # Metodo que mostara la img thubnail si no la encutra mostara otra
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
    image_thub.short_description = 'Imagen'

    def stock(self):
        total = 0
        # Importamos las librerias de Inventario
        from inventario.models import Equipo_Ingreso

        for detalle in Equipo_Ingreso.objects.filter(
                id_equipo=self.id):
                total = total + 1
        if total == 0:
            total = '--'
        else:
            None
        return format_html(
            '<span style="color: #000;">' +
            str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock.short_description = 'Ingresado'

    def disponible(self):
        total = 0
        # Importamos las librerias de Inventario
        from inventario.models import Equipo_Ingreso, Ingreso

        for ingreso in Ingreso.objects.filter(estado=True):
            for detalle in Equipo_Ingreso.objects.filter(
                        id_equipo=self.id, id_ingreso=ingreso):
                        total = total + 1
        return total

    def disponible_color(self):
        total = int(self.disponible())
        if total == 0:
            total = '--'
            color1 = '#D7142B'
            color2 = '#FF7800'
        else:
            if total <= 10:
                color1 = '#D7142B'
                color2 = "#FF7800"
            elif total <= 20:
                color1 = '#FF7800'
                color2 = 'yellow'
            else:
                color1 = '#009A19'
                color2 = '#8AFF00'
        total = (total)
        return format_html(
                    '<span style="color:' + color1 + '; font-weight: bold;' +
                    ' text-shadow: 0px 0px 2px ' + color2 + ';">' +
                    str(total) + '</span>')
    disponible_color.short_description = 'Disponible'

    def asiganado(self):
        total = 0
        return total

    def asignado_color(self):
        total = self.asiganado()
        return total
    asignado_color.short_description = 'Asignado'

    def de_baja(self):
        total = 0
        return total

    def de_baja_color(self):
        total = self.de_baja()
        return total
    de_baja_color.short_description = 'Por dar de Baja'

    def monto_bodega(self):
        total = 0.00
        # Importamos las librerias de Inventario
        from inventario.models import Equipo_Ingreso

        for detalle in Equipo_Ingreso.objects.filter(
                id_equipo=self.id):
                total = total + float(detalle.monto)
        return ("%.2f" % total)

    def monto_bodega_color(self):
        color = '#000'
        total = float(self.monto_bodega())
        if total == 0.00:
            color = '#6B0000'
            total = '---'
        total = str(total)
        return format_html(
                '<span style="color: ' + color + '; font-weight: bold;">Q. ' +
                total + '</span>')
    monto_bodega.short_description = 'Monto Total'

    def info(self):
        ''' Llama al un template que sera drenderizado como un pdf'''
        return mark_safe(
            u'<a class="print" href="/Tarjeta_Kardex_PDF/?id=%s"'
            'target="_blank">'
            '<span class="icon-printer6" align="center"></span></a>'
            % self.id)
    info.short_description = 'T Kardex'

    class Meta:
        ordering = ['nombre']
        verbose_name = "Equipo Didactico"
        verbose_name_plural = "Equipos Didacticos"

    def __str__(self):
        return self.nombre

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
    '''Este metodo elimina de nuestra base de datos una imagen
    de una instancia se esta ya tenia una imagen previa''' 
    # Obtiene la imagen antigua de la instancia en cuestion
    old_instance = Material.objects.get(pk=instance.pk)
    # Borra la imagen de la que se ha seleccionado
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
        # Retorna un enlace en donde se podra visualizar la informacion
        # del material en formato PDF
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
        ''' Retornara una imagen para ser mostrada en al admin del material
        en el catalogo del mismo, si no la encuetra coloca otra por default'''
        # Valida si se le subio imagen al material
        if self.img_thubmnail:
            # Y lo retorna en la lista de materiales
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.img_thubmnail.url, width=50, height=50, ))
        # Si no encuentra mostrar una imagen generica
        else:
            # Y lo retorna en la lista de materiales
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url='/../static/core/img/no-img.jpg', width=50, height=50,))
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
        return total
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock.short_description = 'Ingresado_Color'

    def stock_color(self):
        total = self.stock()
        if total == 0:
            total = '--'
        else:
            None
        return format_html(
            '<span style="color: #000;">' +
            str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock_color.short_description = 'Ingresado'

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
    def asignado_flotante(self):
        '''Regresa la cantidad que se encuentra asignada independientemente
        de a quien este asignado, solamente es una suma para reflejar
        un dato'''
        # Se crea una variable total inicializada en 0
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Asignacion, Material_Asignado

        # Se recorren las asignaciones en donde el estado sea aceptado
        for asignacion in Asignacion.objects.filter(estado=False):
            # Se recorren los materiales asignados haciendo una validacion
            # que estos pertenezcan a la instancia y que sena parte de
            # la asignacion
            for detalle in Material_Asignado.objects.filter(
                        id_material=self.id, id_asignacion=asignacion):
                        # Si los datos coinciden total sera igual a el mas
                        # el dato en el campo cantidad de Material_Asignado
                        total = total + detalle.cantidad
        
        # Para terminar retorna el total
        return total

    # Metodo que devolvera el stock de materiales Asignados
    def asignado_int(self):
        '''Regresa la cantidad que se encuentra asignada independientemente
        de a quien este asignado, solamente es una suma para reflejar un dato'''
        # Se crea una variable total inicializada en 0
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Asignacion, Material_Asignado
        # Se importan los modelos de Devolucion Y Material_Devuelto
        from movimientos.models import Devolucion, Material_Devuelto

        # Se recorren las asignaciones en donde el estado sea aceptado
        for asignacion in Asignacion.objects.filter(estado=True):
            # Se recorren los materiales asignados haciendo una validacion
            # que estos pertenezcan a la instancia y que sena parte de
            # la asignacion
            for detalle in Material_Asignado.objects.filter(
                        id_material=self.id, id_asignacion=asignacion):
                        # Si los datos coinciden total sera igual a el mas
                        # el dato en el campo cantidad de Material_Asignado
                        total = total + detalle.cantidad
        # Se recorren las Devoluciones en donde el estado sea aceptado
        for devolucion in Devolucion.objects.filter(estado=True):
            # Se recorren los materiales devueltos haciendo una validacion
            # que estos pertenezcan a la instancia y que sena parte de
            # la devolucion
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                # Si los datos coinciden total sera igual a el menos
                # el dato en el campo cantidad de Material_Devuelto
                total = total - detalle.total_sum()
        # Para terminar retorna el total
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
        '''Este metodo muestra el total de materiales transformados
        es una salida para el mismo sin darle de baja ya que paso a ser parte
        de otro equipo o bien se encuentra formando parte de un modelo'''
        # Se crea una variable total inicializada en 0
        total = 0
        # se importan los modelos de Devolucion y Material_Devuelto
        from movimientos.models import Devolucion, Material_Devuelto

        # Se recorren las Devoluciones en donde el estado sea aceptado
        for devolucion in Devolucion.objects.filter(estado=True):
            # Se recorren los materiales devueltos haciendo una validacion
            # que estos pertenezcan a la instancia y que sena parte de
            # la devolucion
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                # Si los datos coinciden total sera igual a el mas
                # el dato en el campo transformados de Material_Devuelto
                total = total + detalle.transformados
        # Evalua si total es igual a cero (0)
        if total == 0:
            # Si es igual a cero sustituye el 0 por dos guiones medios
            total = '--'
        # De lo contrario si no es igual
        else:
            # No realizara nada
            None
        # Regresa un texto en formateado en html y se pasa total como variable
        return format_html(
            '<span style="color: #000;">' +
            str(total) + '</span>')
    # Sirve para mostrar la descripción del método en el ADMIN

    transformado.short_description = 'Transformado'

    # Metodo que retorna los materiales consumidos o usados
    def consumido(self):
        '''Retornara los materiales que fueron utilizados para practicas o
        para otros modelos didacticos formando en praticas siendo
        parte aun del inventairo'''
        # Se crea una variable total inicializada en 0
        total = 0
        # se importan los modelos de Devolucion y Material_Devuelto
        from movimientos.models import Devolucion, Material_Devuelto

        # Se recorren las Devoluciones en donde el estado sea aceptado
        for devolucion in Devolucion.objects.filter(estado=True):
            # Se recorren los materiales devueltos haciendo una validacion
            # que estos pertenezcan a la instancia y que sena parte de
            # la devolucion
            for detalle in Material_Devuelto.objects.filter(
                        id_material=self.id, id_devolucion=devolucion):
                # Si los datos coinciden total sera igual a el mas
                # el dato en el campo desechos de Material_Devuelto
                total = total + detalle.desechados
        return total
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    consumido.short_description = 'De Baja'

    def consumido_color(self):
        total = self.consumido()
        # Evalua si total es igual a cero (0)
        if total == 0:
            # Si es igual a cero sustituye el 0 por dos guiones medios
            total = '--'
        # De lo contrario si no es igual
        else:
            # No realizara nada
            None
        # Regresa un texto en formateado en html y se pasa total como variable
        return format_html(
                '<span style="color: #000; text-shadow: 0px 0px 1px #919191;">' +
                str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    consumido_color.short_description = 'De Baja'

    # Metodo que retorna el monto total en bodega
    def monto_bodega(self):
        '''Devuelve el monto de materiales en bodega mostrandose asi
        en listado de que forma nuestro catalogo, tomara los datos
        de dos metodos que ya fueron utilizados con anterioridad
        para aprovechar la reautilzacion del codigo'''
        # Se crea una variable total inicializada en 0
        total = 0
        # Se crea una variable par el subtotal inicializada en 0
        sub = 0
        # Buscamos traer el total de consumidos
        # creamos una variable de consumidos y traemos el metodo
        consumido = self.consumido()
        # traemos el total ingresado a bodega por el metodo stock
        bodega = self.stock()
        # Realizamos la resta del subtotal
        sub = bodega - consumido
        # Traemos modelo importandolo
        from inventario.models import Material_Detalle
        # Traemos el ultimo detalle de ingreso segun el material
        ultimo = Material_Detalle.objects.filter(
            id_material=self.id).last()
        # Recoremos los materiales para comparar con el ultimo
        for material in Material_Detalle.objects.all():
            if material == ultimo:
                total = sub * material.valor_promedio_ponderado()
        return ("%.2f" % total)
        # Validamos que total no sea 0 para mostrar unicamente los 3 guines

    def monto_bodega_color(self):
        total = self.monto_bodega()
        color = '#000'
        if total == 0:
            color = '#6B0000'
            total = '---'

        return format_html(
                '<span style="color: ' + color + '; font-weight: bold;">Q. ' +
                str(total) + '</span>')
    monto_bodega_color.short_description = 'Monto Total'

    # Metodo que devuelve la representacion de la instancia
    def __str__(self):
        '''Este metodo retorna el nombre y la marca se utilza un
        formateo de texto en donde se coloca "%s"para luego ser
        sustituido por un campo o variable'''
        # retorna al terminar el metodo
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

    # Metodo Stock Mostrara la cantidad ingresada
    def stock(self):
        ''''Este metodo servira para llevar un control de cuantos
        materiales o equipos han sido ingresados, esto no define que esten
        disponibles, sin embargo es fundamental para saber el monto'''
        # Se crea una variable total inicializada a 0
        total = 0
        # Importamos las librerias de Inventario
        from inventario.models import Equipo_Ingreso
        # Recorremos los detalles de Equipos Ingresados
        # Filtrando que los equipos sean igual a la instancia
        for detalle in Equipo_Ingreso.objects.filter(
                id_equipo=self.id):
                # Por cada equipo que se encuentre igual a la instancia total aumenta en 1
                total = total + 1
        # Evalua si total es igual a cero (0)
        if total == 0:
            # Si es igual cambia el valor a dos guiones medios, para no mostrar un 0
            total = '--'
        # De lo contrario si no es igual
        else:
            # No realizara nada
            None
        # Metodo que regresa un texto en formateado en html y se pasa total como variable
        return format_html(
            '<span style="color: #000;">' +
            str(total) + '</span>')
    # Sirve para mostrar la descripcion del metodo en el ADMIN
    stock.short_description = 'Ingresado'

    # Evaula cuantos Equipos o Materiales estan disponibles
    def disponible(self):
        '''Por medio de un recorrido y comparacion se evalua
        cuantos equipos o materiales se encuentran disponibles'''
        # Se crea una variable total inicializada a 0
        total = 0
        # Importamos las librerias de Inventario
        from inventario.models import Equipo_Ingreso, Ingreso
        # Se recorre para saber que ingresos estan dispobles
        # comprobandose por el campo estado de ingreso
        for ingreso in Ingreso.objects.filter(estado=True):
            # Se recorren los equipos de cada ingreso en donde
            # el equipo conisida con el ingreso y con la instancia
            for detalle in Equipo_Ingreso.objects.filter(
                        id_equipo=self.id, id_ingreso=ingreso):
                        # por cada equipo que cumpla con el requisito
                        # total aumenta en uno
                        total = total + 1
        total = (total - (self.asignado_int() + self.asignado_flotante() +
            self.de_baja()))
        # Se regresa la variable total ya con el nuevo nuemro
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

    def asignado_flotante(self):
        '''Regresa la cantidad que se encuentra asignada independientemente
        de a quien este asignado, solamente es una suma para
        reflejar un dato'''
        # Se crea una variable total inicializada en 0
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Equipo_Asignado
        # Se recorren los materiales asignados haciendo una validacion
        # que estos pertenezcan a la instancia y que sena parte de
        # la asignacion
        for detalle in Equipo_Asignado.objects.all():
            if detalle.estado() is False:
                if detalle.id_equipo.id_equipo.id == self.id:
                    total = total + 1
            else:
                None
        # Para terminar retorna el total
        return total

    def asignado_int(self):
        '''Regresa la cantidad que se encuentra asignada independientemente
        de a quien este asignado, solamente es una suma para
        reflejar un dato'''
        # Llamamos a Equipo Ingreso
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Equipo_Asignado
        # Se recorren los materiales asignados haciendo una validacion
        # que estos pertenezcan a la instancia y que sena parte de
        # la asignacion
        for detalle in Equipo_Asignado.objects.all():
            if detalle.estado() is True:
                if detalle.id_equipo.id_equipo.id == self.id:
                    total = total + 1
            else:
                None
        total = total - (
            self.de_baja() + self.dev())
        '''# Se recorren las Devoluciones en donde el estado sea aceptado
                                for devolucion in Devolucion.objects.filter(estado=True):
                                    # Se recorren los materiales devueltos haciendo una validacion
                                    # que estos pertenezcan a la instancia y que sena parte de
                                    # la devolucion
                                    for detalle in Material_Devuelto.objects.filter(
                                                id_material=self.id, id_devolucion=devolucion):
                                        # Si los datos coinciden total sera igual a el menos
                                        # el dato en el campo cantidad de Material_Devuelto
                                        total = total - detalle.total_sum()'''
        # Para terminar retorna el total
        return total

    def asignado_color(self):
        total = self.asignado_int()
        return format_html(
                '<span style="color: #265787; text-shadow: 0px 0px 2px #A1E8FD;">' +
                str(total) + '</span>')
    asignado_color.short_description = 'Asignado'

    def dev(self):
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Equipo_Devuelto
        # Se recorren los materiales asignados haciendo una validacion
        # que estos pertenezcan a la instancia y que sena parte de
        # la asignacion
        for detalle in Equipo_Devuelto.objects.all():
            if detalle.estado_dev() is True:
                if detalle.estado != 'Mlo.':
                    if detalle.id_equipo.id_equipo.id == self.id:
                        total = total + 1
        return total

    def de_baja(self):
        total = 0
        # Se importan los modelos de Asignacion y Material_Asignado
        from movimientos.models import Equipo_Devuelto
        # Se recorren los materiales asignados haciendo una validacion
        # que estos pertenezcan a la instancia y que sena parte de
        # la asignacion
        for detalle in Equipo_Devuelto.objects.all():
            if detalle.estado_dev() is True:
                if detalle.estado == 'Mlo.':
                    if detalle.id_equipo.id_equipo.id == self.id:
                        total = total + 1
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
    monto_bodega_color.short_description = 'Monto Total'

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

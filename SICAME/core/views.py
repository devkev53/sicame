from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from catalogo.models import Material, Equipo
from inventario.models import Ingreso
from movimientos.models import Devolucion


class Catalogo_PDF(PDFTemplateView):
    template_name = 'Catalogo.html'

    def get_context_data(self, **kwargs):
        equipo = Equipo.objects.all()
        material = Material.objects.all()

        return super(Catalogo_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            material=material,
            **kwargs
            )


class Movimientos_PDF(PDFTemplateView):
    template_name = 'Movimientos.html'

    def movi(self):
        from movimientos.models import Asignacion, Devolucion
        lista = []
        for asignacion in Asignacion.objects.all():
            if asignacion.devuelto() is False:
                datos = {}
                datos['is'] = 'asig'
                datos['ref'] = asignacion.id_no
                datos['fecha'] = asignacion.fecha
                datos['hora'] = asignacion.hora
                datos['create'] = asignacion.create_by
                datos['to'] = asignacion.assigned_to
                datos['estado'] = asignacion.estado
                datos['monto'] = asignacion.monto_total_format()
                # Adjunto el diccionario a la lista
                lista.append(datos)
        for devo in Devolucion.objects.all():
            datos = {}
            datos['is'] = 'devo'
            datos['ref'] = devo.id_no
            datos['fecha'] = devo.fecha
            datos['hora'] = devo.hora
            datos['create'] = devo.create_by
            datos['to'] = devo.assigned_to
            datos['estado'] = devo.estado
            datos['monto'] = devo.monto_total()
            # Adjunto el diccionario a la lista
            lista.append(datos)
        # Ordeno la Lista
        lista = sorted(lista, key=lambda k: k['fecha'])
        return lista

    def get_context_data(self, **kwargs):
        lista = self.movi()

        return super(Movimientos_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            lista=lista,
            **kwargs
            )


class Ingresos_Egresos_PDF(PDFTemplateView):
    template_name = 'Ingresos_egresos.html'

    def in_out(self):
        '''Este Metodo sirve para recorrecer los Ingresos y las
        Devoluciones creando una lista de diccionarios y ordenarla
        por las fechas de ingreso y salidas'''
        # creo una lista para guardar los diccionarios
        lista = []
        # Recorro los ingresos
        for ingreso in Ingreso.objects.all():
            # Creo un diccionario de datos
            datos = {}
            # Lleno el diccionario con cada ingreso reccorido
            datos['is'] = 'in'
            datos['ref'] = ingreso.ref()
            datos['creado'] = ingreso.create_by.user
            datos['fecha'] = ingreso.fecha
            datos['hora'] = ingreso.hora
            datos['estado'] = ingreso.estado
            datos['monto'] = ingreso.monto_ingreso()
            # Adjunto el diccionario a la lista
            lista.append(datos)
        # Recorro las Devoluciones para agregar como egresos
        for devolucion in Devolucion.objects.all():
            # verifico si tiene egresos para validar
            if devolucion.if_out() == True:
                # Creo nuevamente el diccionario
                datos = {}
                # LLeno el diccionario con cada devolucion recorrida
                datos['is'] = 'out'
                datos['ref'] = devolucion.id_no
                datos['creado'] = devolucion.create_by.user
                datos['fecha'] = devolucion.fecha
                datos['hora'] = devolucion.hora
                datos['estado'] = devolucion.estado
                datos['monto'] = devolucion.monto_desecho()
                # Adjunto el diccionario a la lista
                lista.append(datos)
        # Ordeno la Lista
        lista = sorted(lista, key=lambda k: k['fecha'])
        # Retorno la Lista
        return lista

    def t_ingresos(self):
        '''Metodo que servira para sumar los ingresos y restar
        los egresos que se dan por medio de las devoluciones'''
        total = 0
        lista = self.in_out()
        for datos in lista:
            if datos.get('is') == 'in':
                total = total + datos.get('monto')
            else:
                total = total - datos.get('monto')
        return total

    def get_context_data(self, **kwargs):
        total = self.t_ingresos
        datos = self.in_out

        return super(Ingresos_Egresos_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            datos=datos,
            total=total,
            **kwargs
            )

from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Material, Equipo
from inventario.models import Ingreso, Material_Detalle, Equipo_Ingreso
from movimientos.models import Devolucion, Material_Devuelto

# Create your views here.


class Ficha_Kardex_PDF(PDFTemplateView):
    template_name = 'Kardex_Material.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        material = Material.objects.get(id=ids)
        detalle = Material_Detalle.objects.filter(id_material=ids)
        devolucion = Material_Devuelto.objects.filter(
            id_material=ids)

        lista = []
        for ingreso in Material_Detalle.objects.filter(id_material=ids):
            datos = {}
            datos['is'] = 'in'
            datos['ref'] = ingreso.id_ingreso.ref()
            datos['fecha'] = ingreso.id_ingreso.fecha
            datos['hora'] = ingreso.id_ingreso.hora
            datos['estado'] = ingreso.estado
            datos['valor_u'] = ingreso.por_unidad()
            datos['in_cant'] = ingreso.cantidad
            datos['in_val'] = ingreso.monto
            datos['out_cant'] = '---'
            datos['out_val'] = '---'
            datos['saldo_cant'] = ingreso.saldo_cantidad()
            datos['saldo_val'] = ingreso.saldo_valores()
            datos['promedio'] = ingreso.valor_promedio_ponderado()
            lista.append(datos)

        for egreso in Material_Devuelto.objects.filter(id_material=ids):
            # verifico si tiene egresos para validar
            if egreso.desechados > 0:
                if egreso.id_devolucion.estado is True:
                    datos = {}
                    datos['is'] = 'out'
                    datos['ref'] = egreso.id_devolucion.set_referncia()
                    datos['fecha'] = egreso.id_devolucion.fecha
                    datos['hora'] = egreso.id_devolucion.hora
                    datos['estado'] = egreso.id_devolucion.estado
                    datos['valor_u'] = egreso.valor_por_unidad()
                    datos['in_cant'] = '---'
                    datos['in_val'] = '---'
                    datos['out_cant'] = egreso.desechados
                    datos['out_val'] = egreso.saldo_desechados()
                    datos['saldo_cant'] = egreso.saldo_cantidad()
                    datos['saldo_val'] = egreso.saldo_valores()
                    datos['promedio'] = egreso.vpp()
                    lista.append(datos)

        # Ordeno la Lista
        lista = sorted(lista, key=lambda k: k['fecha'])
        # obtener el ultimo detalle de ingreso
        ultimo = Material_Detalle.objects.filter(id_material=ids).last()
        cantidad = lista[-1]

        return super(Ficha_Kardex_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Kardex',
            detalle=detalle,
            devolucion=devolucion,
            lista=lista,
            ultimo=ultimo,
            material=material,
            cantidad=cantidad,
            **kwargs
            )


class Tarjeta_Kardex_Equipo_PDF(PDFTemplateView):
    template_name = 'Kardex_Equipo.html'

    def get_context_data(self, **kwargs):

        ids = self.request.GET.get('id')
        material = Equipo.objects.get(id=ids)
        detalle = Equipo_Ingreso.objects.filter(id_equipo=ids)

        # obtener el ultimo detalle de ingreso
        ultimo = Material_Detalle.objects.filter(id_material=ids).last()

        return super(Tarjeta_Kardex_Equipo_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Kardex',
            detalle=detalle,
            ultimo=ultimo,
            material=material,
            **kwargs
            )

'''fecha=None, detalle=None, estado=None, valor_u=None,
            e_cant=None, e_val=None, s_cant=None, s_val=None,
            cant=None, val=None, prome=None'''


class Listado_Equipos(PDFTemplateView):
    template_name = 'Lista_de_Equipos.html'

    def get_context_data(self, **kwargs):
        equipo = Equipo.objects.all()

        return super(Listado_Equipos, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            **kwargs
            )


class Listado_Materiales(PDFTemplateView):
    template_name = 'Lista_de_Materiales.html'

    def get_context_data(self, **kwargs):
        equipo = Material.objects.all()

        return super(Listado_Materiales, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            **kwargs
            )

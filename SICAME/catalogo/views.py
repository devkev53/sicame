from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Material, Equipo
from inventario.models import Ingreso, Material_Detalle, Equipo_Ingreso
from movimientos.models import Devolucion, Material_Devuelto

# Create your views here.


class Ficha_Kardex_PDF(PDFTemplateView):
    template_name = 'Kardex_Material.html'

    def get_context_data(self, **kwargs):
        dic_Kardex = {}

        ids = self.request.GET.get('id')
        material = Material.objects.get(id=ids)
        detalle = Material_Detalle.objects.filter(id_material=ids)
        devolucion = Material_Devuelto.objects.filter(
            id_material=ids)

        # obtener el ultimo detalle de ingreso
        ultimo = Material_Detalle.objects.filter(id_material=ids).last()

        return super(Ficha_Kardex_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Kardex',
            detalle=detalle,
            devolucion=devolucion,
            ultimo=ultimo,
            material=material,
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


class Listado_Material(PDFTemplateView):
    template_name = 'Kardex_Material.html'

    def get_context_data(self, **kwargs):
        material = Material.objects.all()

        return super(Ficha_Kardex_PDF, self).get_context_data(
            pagesize='Legal landscape',
            material=material,
            **kwargs
            )

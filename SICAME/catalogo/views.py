from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Material
from inventario.models import Ingreso, Material_Detalle

# Create your views here.


class Ficha_Kardex_PDF(PDFTemplateView):
    template_name = 'Kardex_Material.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        material = Material.objects.get(id=ids)
        detalle = Material_Detalle.objects.filter(id_material=ids)

        # obtener el ultimo detalle de ingreso
        ultimo = Material_Detalle.objects.filter(id_material=ids).last()

        return super(Ficha_Kardex_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Kardex',
            detalle=detalle,
            ultimo=ultimo,
            material=material,
            **kwargs
            )

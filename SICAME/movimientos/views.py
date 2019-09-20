from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Asignacion, Material_Asignado
from inventario.models import Material_Detalle
from catalogo.models import Material

# Create your views here.


class Asignacion_PDF(PDFTemplateView):
    template_name = 'asignacion.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        asignacion = Asignacion.objects.get(id_no=ids)
        detalle = Material_Asignado.objects.filter(id_asignacion=ids)

        return super(Asignacion_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Asignacion',
            detalle=detalle,
            asignacion=asignacion,
            **kwargs
            )

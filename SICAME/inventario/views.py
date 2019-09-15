from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from django.contrib.auth.models import User
from .models import *

# Create your views here.


class Ingreso_PDF(PDFTemplateView):
    template_name = 'Ingreso.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        ingreso = Ingreso.objects.get(id=ids)
        detalle = Material_Detalle.objects.filter(id_ingreso=ids)

        return super(Ingreso_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            detalle=detalle,
            ingreso=ingreso,
            **kwargs
            )

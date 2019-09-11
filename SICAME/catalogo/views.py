from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Material

# Create your views here.


class Ficha_Kardex_PDF(PDFTemplateView):
    template_name = 'Kardex_Material.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        material = Material.objects.get(id=ids)

        return super(Ficha_Kardex_PDF, self).get_context_data(
            pagesize='Letter',
            title='Kardex',
            material=material,
            **kwargs
            )

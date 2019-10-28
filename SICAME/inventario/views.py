from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from django.contrib.auth.models import User
from .models import *

# Create your views here.


class Ingreso_PDF(PDFTemplateView):
    template_name = 'Ingreso.html'

    def total(self):
        total_in = 0.0
        ids = self.request.GET.get('id')
        for detalle in Material_Detalle.objects.filter(id_ingreso=ids):
            total_in = total_in + float(detalle.monto)
        for Equipo in Equipo_Ingreso.objects.filter(id_ingreso=ids):
            total_in = total_in + float(Equipo.monto)
        return ("%.2f" % total_in)

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        ingreso = Ingreso.objects.get(id=ids)
        detalle = Material_Detalle.objects.filter(id_ingreso=ids)
        equipo = Equipo_Ingreso.objects.filter(id_ingreso=ids)
        total = self.total()

        return super(Ingreso_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            total=total,
            detalle=detalle,
            ingreso=ingreso,
            equipo=equipo,
            **kwargs
            )


class Listado_Ingresos(PDFTemplateView):
    template_name = 'Lista_de_Ingresos.html'

    def get_context_data(self, **kwargs):
        equipo = Ingreso.objects.all()

        return super(Listado_Ingresos, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            **kwargs
            )


class Listado_Detalle_Materiales(PDFTemplateView):
    template_name = 'Lista_de_Detalle_Materiales.html'

    def get_context_data(self, **kwargs):
        equipo = Material.objects.all()

        return super(Listado_Detalle_Materiales, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            **kwargs
            )


class Listado_Detalle_Equipos(PDFTemplateView):
    template_name = 'Lista_de_Detalle_Equipos.html'

    def get_context_data(self, **kwargs):
        equipo = Material.objects.all()

        return super(Listado_Detalle_Equipos, self).get_context_data(
            pagesize='Legal landscape',
            title='Ingreso',
            equipo=equipo,
            **kwargs
            )

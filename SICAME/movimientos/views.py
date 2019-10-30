from django.shortcuts import render

from easy_pdf.views import PDFTemplateView
from .models import Asignacion, Material_Asignado, Equipo_Asignado
from .models import Devolucion, Material_Devuelto, Equipo_Devuelto
from inventario.models import Material_Detalle
from catalogo.models import Material

# Create your views here.


class Asignacion_PDF(PDFTemplateView):
    template_name = 'asignacion.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        asignacion = Asignacion.objects.get(id_no=ids)
        detalle = Material_Asignado.objects.filter(id_asignacion=ids)
        equipo = Equipo_Asignado.objects.filter(id_asignacion=ids)
        n_materiales = 0
        for materiales in detalle:
            n_materiales = n_materiales + 1
        n_equipo = 0
        for equipos in equipo:
            n_equipo = n_equipo + 1
        estado = asignacion.estado_asig_dev()

        return super(Asignacion_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Asignacion',
            detalle=detalle,
            estado=estado,
            asignacion=asignacion,
            equipo=equipo,
            nm=n_materiales,
            ne=n_equipo,
            **kwargs
            )


class Devolucion_PDF(PDFTemplateView):
    template_name = 'devolucion.html'

    def get_context_data(self, **kwargs):
        ids = self.request.GET.get('id')
        devolucion = Devolucion.objects.get(id_no=ids)
        detalle = Material_Devuelto.objects.filter(id_devolucion=ids)
        equipo = Equipo_Devuelto.objects.filter(id_devolucion=ids)
        n_materiales = 0
        for materiales in detalle:
            n_materiales = n_materiales + 1
        n_equipo = 0
        for equipos in equipo:
            n_equipo = n_equipo + 1

        return super(Devolucion_PDF, self).get_context_data(
            pagesize='Legal landscape',
            title='Asignacion',
            detalle=detalle,
            devolucion=devolucion,
            equipo=equipo,
            nm=n_materiales,
            ne=n_equipo,
            **kwargs
            )

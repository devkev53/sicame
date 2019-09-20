from django.urls import path
from django.conf.urls import url
# Llamando a las views de registros
from .views import Asignacion_PDF


urlpatterns = [
    # -- URL PATH DE LOS PDFS
    # path de detalle de ingresos
    url(r"^Detalle/(?P<id>)", Asignacion_PDF.as_view(), name='detallePDF'),
]

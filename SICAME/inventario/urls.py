from django.urls import path
from django.conf.urls import url
# Llamando a las views de registros
from .views import Ingreso_PDF
from django.conf.urls import url


urlpatterns = [
   url(r"^Ingreso_PDF/(?P<id>)", Ingreso_PDF.as_view(), name='ingerso_pdf'),
    # path('<int:id>/', Listado_Material.as_view(), name='listadoPDF'),
]

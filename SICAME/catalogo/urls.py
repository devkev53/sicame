from django.urls import path
from django.conf.urls import url
# Llamando a las views de registros
from .views import *


urlpatterns = [
    # -- URL PATH DE LOS PDFS
    # path de detalle de ingresos
    url(r"^Ficha_Kardex_PDF/(?P<id>)", Ficha_Kardex_PDF.as_view()),
]

from django.urls import path
from django.conf.urls import url
# Llamando a las views de registros
from .views import T_Responsabilidad_PDF
from django.conf.urls import url


urlpatterns = [
   url(
    r"^Tarjeta_de_Responsabilidad_PDF/(?P<id>)",
    T_Responsabilidad_PDF.as_view(), name='tarjeta_R'),
]

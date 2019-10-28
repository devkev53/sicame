# Importacion del modulo path
from django.urls import path
# Importaciin del modulo url
from django.conf.urls import url
# Llamando a las vistas(views) de catalago
'''Cuando solo se coloca un "." se hace refernecia
la misma carpeta y el "*" importa todas las clases'''
from .views import *


# Se crea el conjunto de urls
urlpatterns = [
    # -- URL PATH DE LOS PDFS
    # path de detalle de ingresos
    # Se coloca la url que se usuar, seguido de la clase que llama a los parametros
    url(r"^Ficha_Kardex_PDF/(?P<id>)", Ficha_Kardex_PDF.as_view()),
    # path de la tarjeta kardex
    url(r"^Tarjeta_Kardex_PDF/(?P<id>)", Tarjeta_Kardex_Equipo_PDF.as_view()),
    # path para la impresion de listado de equipos
    url(r"^Listado_Equipos_PDF/", Listado_Equipos.as_view()),
    # path para la impresion de listado de materiales
    url(r"^Listado_Materiales_PDF/", Listado_Materiales.as_view(),
        name='list_materiales'),
]

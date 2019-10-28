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
    # path para la impresion informe de Catalogo
    url(r"^Catalogo_PDF/", Catalogo_PDF.as_view(),
        name='catalogo-PDF'),
    # path para la impresion informe de Catalogo
    url(r"^Ingresos_Egresos_PDF/", Ingresos_Egresos_PDF.as_view(),
        name='informe 2'),
]

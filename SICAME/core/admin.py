from django.contrib import admin
from .models import *

# Register your models here.


# Clase que permite modificar la repsesentacion del modelo en el admin
class Admin_Marca(admin.ModelAdmin):
    # Agrega un buscador al modelo, segun los campos que se indiquen
    search_fields = ['nombre']
    # Ordena las instancias segun los campos que se indiquen
    ordering = ['nombre']

admin.site.register(Marca, Admin_Marca)
admin.site.register(Categoria)

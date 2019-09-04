from django.contrib import admin
from .models import *

# Register your models here.


class AdminMaterial(admin.ModelAdmin):
    list_display = [
        'nombre', 'image_thub', 'id_Marca', 'id_Categoria',
        'stock', 'disponible', 'asignado', 'transformado',
        'monto_bodega']
    list_filter = ['id_Marca', 'id_Categoria']
    search_fields = ['nombre']
    list_display_links = ('nombre', 'image_thub',)

admin.site.register(Material, AdminMaterial)

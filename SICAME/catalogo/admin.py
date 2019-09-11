from django.contrib import admin
from .models import *

# Register your models here.


class AdminMaterial(admin.ModelAdmin):
    list_display = [
        'nombre', 'image_thub', 'id_Marca',
        'stock', 'disponible', 'asignado', 'transformado',
        'monto_bodega', 'ficha']
    list_filter = ['id_Marca', 'id_Categoria']
    search_fields = ['nombre']
    list_display_links = ('nombre', 'image_thub',)
    list_per_page = 10

admin.site.register(Material, AdminMaterial)

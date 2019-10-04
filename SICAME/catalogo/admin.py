from django.contrib import admin
from .models import *

# Register your models here.


class AdminMaterial(admin.ModelAdmin):
    list_display = [
        'nombre', 'image_thub', 'id_Marca',
        'stock', 'disponible', 'asignado', 'transformado',
        'consumido', 'monto_bodega', 'ficha']
    list_filter = ['id_Marca', 'id_Categoria']
    search_fields = ['nombre']
    list_display_links = ('nombre', 'image_thub',)
    list_per_page = 10
    actions = ['listado_pdf']

    def listado_pdf(self, request, queryset):
        queryset.all()
        self.message_user(
            request, 'Se ha realizado la Impresion de Materiales')
    listado_pdf.short_description = 'Imprimir Listado de Material'


class AdminEquipo(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ((
                'nombre', 'id_Marca', 'id_Categoria', 'img'), (
                'descripcion'))
        }),)
    list_display = [
        'nombre', 'image_thub', 'stock',
        'disponible_color', 'asignado_color', 'de_baja_color',
        'monto_bodega_color', 'info']
    list_filter = ['id_Categoria']
    search_fields = ['nombre']
    list_display_links = ('nombre', 'image_thub',)
    list_per_page = 10
    actions = ['listado_pdf']


admin.site.register(Material, AdminMaterial)
admin.site.register(Equipo, AdminEquipo)

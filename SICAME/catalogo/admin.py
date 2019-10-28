from django.contrib import admin
from django.shortcuts import redirect
from .models import *

# Register your models here.


class AdminMaterial(admin.ModelAdmin):
    # Permite ordenar los campos del formualario del modelo
    fieldsets = (
        (None, {
            'fields': ((
                'nombre', 'id_Marca', 'id_Categoria', 'img'), (
                'descripcion'))
        }),)
    list_display = [
        'nombre', 'image_thub', 'id_Marca',
        'stock_color', 'disponible', 'asignado', 'transformado',
        'consumido_color', 'monto_bodega_color', 'ficha']
    list_filter = ['id_Marca', 'id_Categoria']
    search_fields = ['nombre']
    list_display_links = ('nombre', 'image_thub',)
    list_per_page = 10
    actions = ['listado_materiales']

    def listado_materiales(self, request, queryset):
        return redirect('/Listado_Materiales_PDF')
    listado_materiales.short_description = 'Imprimir Listado'


# Clase que permite modificar la repsesentacion del modelo en el admin
class AdminEquipo(admin.ModelAdmin):
    # Permite ordenar los campos del formualario del modelo
    fieldsets = (
        (None, {
            'fields': ((
                'nombre', 'id_Marca', 'id_Categoria', 'img'), (
                'descripcion'))
        }),)
    # Es una Lista de los campos que se mostraran por cada instancia
    list_display = [
        'nombre', 'image_thub', 'stock',
        'disponible_color', 'asignado_color', 'de_baja_color',
        'monto_bodega_color', 'info']
    # Permite agregar un filtro para el modelo, por medio de sus campos
    list_filter = ['id_Categoria']
    # Agrega un buscador al modelo, segun los campos que se indiquen
    search_fields = ['nombre']
    # Es un listado de campos que seran un link para editar la instancia
    list_display_links = ('nombre', 'image_thub',)
    # Agrega un paginador segun el numero de instancias que se coloque
    list_per_page = 10
    # Muestra un cuadro de seleccion con las acciones que se le indiquen
    actions = ['listado_equipo']

    def listado_equipo(self, request, queryset):
        return redirect('/Listado_Equipos_PDF')
    listado_equipo.short_description = 'Imprimir Listado'


admin.site.register(Material, AdminMaterial)
admin.site.register(Equipo, AdminEquipo)

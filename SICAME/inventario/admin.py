from django.contrib import admin
from .models import *

# Register your models here.


class Material_DetalleInline(admin.TabularInline):
    model = Material_Detalle
    extra = 0
    # raw_id_fields = (,)
    fieldsets = (
        (None, {
            'fields': (('id_material', 'cantidad', 'monto', 'ubicacion'), (
                ))
        }),)


class AdminMaterial_Detalle(admin.ModelAdmin):
    readonly_fields = [
        'id_ingreso', 'id_material', 'cantidad', 'monto',
        'por_unidad', 'ubicacion']
    fieldsets = (
        ('Registrar nuevo Ingreso a Inventario', {
            'fields': (('id_ingreso',), (
                'id_material', 'cantidad', 'monto', 'por_unidad', 'ubicacion'))
        }),)
    list_display = [
        'ref_m', 'id_material', 'cantidad', 'por_unidad',
        'ubicacion']
    search_fields = ['id_material__nombre', 'ref_m']


class AdminIngreso(admin.ModelAdmin):
    inlines = [Material_DetalleInline]
    readonly_fields = ['fecha', 'hora']
    fieldsets = (
        ('Registrar nuevo Ingreso a Inventario', {
            'fields': (('create_by', 'fecha', 'hora', 'referencia'), (
                ))
        }),)
    list_display = [
        'id', 'ref', 'create_by', 'fecha',
        'hora', 'estado']
    search_fields = ['referencia', 'fecha', 'create_by']
    list_display_links = ('ref', )
    actions = []

    # Funcion para que la fk author seleccione al usuario logueado
    def get_form(self, request, *args, **kwargs):
        form = super(AdminIngreso, self).get_form(
            request, *args, **kwargs)
        form.base_fields['create_by'].initial = request.user
        return form

admin.site.register(Ingreso, AdminIngreso)
admin.site.register(Material_Detalle, AdminMaterial_Detalle)

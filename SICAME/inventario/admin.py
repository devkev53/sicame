from django.contrib import admin
from .models import *

# Register your models here.


class Material_DetalleInline(admin.TabularInline):
    model = Material_Detalle
    extra = 1
    raw_id_fields = ('id_material',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_material']
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
        'ref_m', 'fecha_ingreso', 'id_material', 'cantidad', 'por_unidad',
        'ubicacion']
    search_fields = ['id_material', 'ref_m']
    list_filter = ['id_ingreso__fecha', 'id_ingreso__referencia']


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
    search_fields = ['referencia']
    list_filter = ['create_by', 'fecha']
    list_display_links = ('ref', )
    actions = ['disponible_update']

    def disponible_update(self, request, queryset):
        for row in queryset.filter(estado=False):
            self.log_change(request, row, 'Cambiar a disponible')
        rows_updated = 0

        for obj in queryset:
            if not obj.estado:
                obj.estado = True
                obj.save()

                rows_updated += 1

        if rows_updated == 1:
            message_bit = 'Se cambio un Ingrese'
        else:
            message_bit = '%s Ingresos fueron cambiadas' % rows_updated
        self.message_user(
            request, '%s satisfactoriamente como disponibles' % message_bit)
    disponible_update.short_description = 'Cambiar a disponible'

    # Funcion para que la fk author seleccione al usuario logueado
    def get_form(self, request, *args, **kwargs):
        form = super(AdminIngreso, self).get_form(
            request, *args, **kwargs)
        form.base_fields['create_by'].initial = request.user
        return form


class AdminAsignacion(admin.ModelAdmin):
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
    search_fields = ['referencia']
    list_filter = ['create_by', 'fecha']
    list_display_links = ('ref', )
    actions = ['disponible_update']

admin.site.register(Ingreso, AdminIngreso)
admin.site.register(Asignacion, AdminAsignacion)
admin.site.register(Material_Detalle, AdminMaterial_Detalle)

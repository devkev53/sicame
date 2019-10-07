from django.contrib import admin
from .models import *

# Register your models here.


class Material_DetalleInline(admin.TabularInline):
    model = Material_Detalle
    extra = 0
    min_num = 0
    raw_id_fields = ('id_material',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_material']
    fieldsets = (
        (None, {
            'fields': (('id_material', 'cantidad', 'monto', 'ubicacion'), (
                ))
        }),)


class Equipo_IngresoInline(admin.StackedInline):
    model = Equipo_Ingreso
    extra = 0
    min_num = 0
    raw_id_fields = ('id_equipo',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_equipo']
    fieldsets = (
        (None, {
            'fields': ((
                'ibe', 'id_equipo',), (
                'id_Marca', 'modelo', 'serie',), (
                'monto', 'ubicacion'), (
                ))
        }),)


class Admin_Equipo_Ingreso(admin.ModelAdmin):
    list_display = ['ibe', 'id_equipo', 'id_Marca', 'modelo', 'serie', 'monto']
    search_fields = ['id_material', 'ref_m']
    autocomplete_fields = ['id_equipo', 'id_Marca']
    list_filter = ['id_equipo', 'id_Marca']


class AdminMaterial_Detalle(admin.ModelAdmin):
    readonly_fields = [
        'id_ingreso', 'id_material', 'cantidad', 'monto',
        'por_unidad', 'ubicacion']
    fieldsets = (
        (None, {
            'fields': (('id_ingreso',), (
                'id_material', 'cantidad', 'monto', 'por_unidad', 'ubicacion'))
        }),)
    list_display = [
        'ref_m', 'fecha_ingreso', 'id_material', 'cantidad', 'por_unidad',
        'ubicacion', 'valor_promedio_ponderado_str']
    search_fields = ['id_material', 'ref_m']
    list_filter = ['id_ingreso__fecha', 'id_ingreso__referencia']


class AdminIngreso(admin.ModelAdmin):
    inlines = [Material_DetalleInline, Equipo_IngresoInline]
    readonly_fields = ['create_by', 'fecha', 'hora']
    fieldsets = (
        (None, {
            'fields': ((
                'create_by', 'fecha', 'hora', 'referencia', 'descripcion'), (
                ))
        }),)
    list_display = [
        'id', 'ref', 'create_by', 'fecha',
        'hora', 'estado', 'boleta']
    search_fields = ['referencia']
    list_filter = ['create_by', 'fecha']
    list_display_links = ('ref', )
    actions = ['disponible_update']
    # Nos permite editar cualquier campo de la instancia desde
    # la vsta con el listado de instanacias creadas
    list_editable = []
    # Cuando editamos una instancia ya creada remplaza el
    # Guardar por un guardar como nuevo si este esta en True
    save_as = False

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
    def save_model(self, request, obj, form, change):
        re_user = request.user
        perfil = Perfil.objects.filter(user=re_user).get()
        obj.create_by = perfil
        super().save_model(request, obj, form, change)

    # Funcion para que la fk author seleccione al usuario logueado
    # def get_form(self, request, *args, **kwargs):
    #     form = super(AdminIngreso, self).get_form(
    #         request, *args, **kwargs)
    #     form.base_fields['create_by'].initial = request.user
    #     return form

admin.site.register(Ingreso, AdminIngreso)
admin.site.register(Material_Detalle, AdminMaterial_Detalle)
admin.site.register(Equipo_Ingreso, Admin_Equipo_Ingreso)

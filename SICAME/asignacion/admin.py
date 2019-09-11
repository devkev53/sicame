from django.contrib import admin
from .models import *

# Register your models here.

class Material_Asig_Inline(admin.TabularInline):
    model = Material_Asig
    extra = 1
    raw_id_fields = ('id_material',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_material']
    fieldsets = (
        (None, {
            'fields': (('id_material', 'cantidad', 'ubicacion'), (
                ))
        }),)


class AdminAsignacion(admin.ModelAdmin):
    inlines = [Material_Asig_Inline, ]
    readonly_fields = ['create_by', 'asig_id', 'fecha', 'hora']
    fieldsets = (
        ('Registrar nuevo Ingreso a Inventario', {
            'fields': (('asig_id', 'create_by', 'fecha', 'hora'), (
                'assigned_to', 'module'))
        }),)
    list_display = [
        'asig_id', 'create_by', 'fecha',
        'hora', 'assigned_to', 'estado_color']
    search_fields = ['asig_id']
    list_filter = ['create_by', 'fecha']
    list_display_links = ('asig_id', )
    actions = ['disponible_update']

    # Funcion para que la fk author seleccione al usuario logueado
    def save_model(self, request, obj, form, change):
        re_user = request.user
        perfil = Perfil.objects.filter(user=re_user).get()
        obj .create_by = perfil
        super().save_model(request, obj, form, change)

admin.site.register(Asignacion, AdminAsignacion)
admin.site.register(Material_Asig)

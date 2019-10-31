from django.contrib import admin
from .models import *

# Register your models here.


class AdminPerfil(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ((
                'user'), (
                'foto', 'direccion'), (
                'telefono', 'puesto'))
        }),)
    list_display = [
        'image_thub', 'full_name',
        'material_asignado', 'equipo_asignado', 'total_asignado', 'tarjeta']
    list_filter = []
    search_fields = [
        'nombre', 'user',
        'user__first_name', 'user__last_name']
    list_display_links = ('image_thub',)


class AdminMi_Perfil(admin.ModelAdmin):
    readonly_fields = ['user']
    fieldsets = (
        (None, {
            'fields': ((
                'user'), (
                'foto', 'direccion'), (
                'telefono', 'puesto'))
        }),)
    list_display = [
        'image_thub', 'full_name',
        'material_asignado', 'equipo_asignado', 'total_asignado', 'tarjeta']
    list_filter = []
    search_fields = [
        'nombre', 'user',
        'user__first_name', 'user__last_name']
    list_display_links = ('image_thub',)

    # Funcion para filtrar contenido por usuario
    def get_queryset(self, request, *args, **kwargs):
        qs = super(AdminMi_Perfil, self).get_queryset(
            request, *args, **kwargs)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Perfil, AdminPerfil)
admin.site.register(Mi_Perfil, AdminMi_Perfil)

from django.contrib import admin
from .models import *

# Register your models here.


class AdminPerfil(admin.ModelAdmin):
    list_display = [
        'image_thub', 'full_name',
        'material_asignado', 'equipo_asignado', 'Total_asignado']
    list_filter = []
    search_fields = [
        'nombre', 'user',
        'user__first_name', 'user__last_name']
    list_display_links = ('image_thub',)

admin.site.register(Perfil, AdminPerfil)

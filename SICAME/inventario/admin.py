from django.contrib import admin
from .models import *

# Register your models here.


class AdminIngreso(admin.ModelAdmin):
    readonly_fields = ['fecha', 'hora']
    fieldsets = (
        ('Registrar nuevo Ingreso a Inventario', {
            'fields': (('create_by', 'fecha', 'hora', 'referencia'), (
                ))
        }),)
    list_display = [
        'id', 'referencia', 'create_by', 'fecha',
        'hora']
    search_fields = ['referencia', 'fecha', 'create_by']
    list_display_links = ('referencia',)
    actions = []

    # Funcion para que la fk author seleccione al usuario logueado
    def get_form(self, request, *args, **kwargs):
        form = super(AdminIngreso, self).get_form(
            request, *args, **kwargs)
        form.base_fields['create_by'].initial = request.user
        return form

admin.site.register(Ingreso, AdminIngreso)

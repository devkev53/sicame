from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from registration.models import Perfil

# Importacion que nos permite maquetar o formatear
# con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html

# Register your models here.


class Material_AsignadoInline(admin.TabularInline):
    model = Material_Asignado
    extra = 0
    raw_id_fields = ('id_material',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_material']
    fieldsets = (
        (None, {
            'fields': (('id_material', 'cantidad', 'ubicacion'), (
                ))
        }),)


class Equipo_Asignado_Inline(admin.TabularInline):
    model = Equipo_Asignado
    extra = 0
    raw_id_fields = ('id_equipo',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_equipo']
    fieldsets = (
        (None, {
            'fields': (('id_equipo'), (
                ))
        }),)


class AdminMaterial_Asignado(admin.ModelAdmin):
    list_display = ['id_asig', 'id_material', 'cantidad', 'monto']
    list_filter = ['id_asignacion__fecha', 'id_asignacion__estado']


class AdminAsignacion(admin.ModelAdmin):
    inlines = [Material_AsignadoInline, Equipo_Asignado_Inline]
    readonly_fields = ['create_by', 'id_no', 'fecha', 'hora']
    fieldsets = (
        (None, {
            'fields': (('id_no', 'create_by', 'fecha', 'hora'), (
                'assigned_to', 'module'))
        }),)
    list_display = [
        'id_no', 'create_by', 'fecha',
        'hora', 'asignado', 'estado_color', 'monto_total', 'detalle']
    search_fields = ['id_no']
    list_filter = ['assigned_to', 'fecha']
    list_display_links = ('id_no', )
    actions = ['aceptar_asignacion']

    def get_queryset(self, request, *args, **kwargs):
        ''' -- Funcion que se encarga de filtar el contenido
        en de que usuario sea igual al usuario logeado -- '''
        qs = super(AdminAsignacion, self).get_queryset(
            request, *args, **kwargs)
        log_perfil = Perfil.objects.filter(user=request.user).get()
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Administradores').exists():
            return qs
        else:
            return qs.filter(assigned_to=log_perfil)

    def aceptar_asignacion(self, request, queryset, *args, **kwargs):
        ''' -- Funcion que se encarga modificar y aceptar las asignaciones
        que le ha realizado el administrador de bodega -- '''
        log_perfil = Perfil.objects.filter(user=request.user).get()
        qs = super(AdminAsignacion, self).get_queryset(
            request, *args, **kwargs)
        if qs.filter(assigned_to=log_perfil):
            pass
            for row in queryset.filter(estado=False):
                self.log_change(request, row, 'Aceptar Asignacion')
            rows_updated = 0

            for obj in queryset:
                if not obj.estado:
                    obj.estado = True
                    obj.save()

                    rows_updated += 1

            if rows_updated == 1:
                message_bit = 'Se aceptado una Asignacion'
            else:
                message_bit = '%s Asignaciones fueno aceptadas' % rows_updated
            self.message_user(
                request, '%s satisfactoriamente como aceptadas' % message_bit)
        else:
            self.message_user(
                request, format_html(
                    '<span class="icon-error_outline"'
                    'style="color: black; font-weight: bold;'
                    'text-shadow: 0px 0px 2px #FF0220; '
                    'padding-right: 10px; font-size:22px;"></span>'
                    '<span style="color: black; font-weight: bold;'
                    'text-shadow: 0px 0px 2px #FF0220;'
                    'text-transform: uppercase; font-size:22px;">'
                    'Solamente pueden ser aceptadas por la persona '
                    'a quien se asigno</span>'))
    aceptar_asignacion.short_description = 'Aceptar Asignacion'

    # Funcion para que la fk author seleccione al usuario logueado
    def save_model(self, request, obj, form, change):
        re_user = request.user
        perfil = Perfil.objects.filter(user=re_user).get()
        obj .create_by = perfil
        super().save_model(request, obj, form, change)


class Material_DevueltoInline(admin.StackedInline):
    model = Material_Devuelto
    extra = 0
    raw_id_fields = ('id_material',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_material']
    fieldsets = (
        (None, {
            'fields': ((
                'id_material',), (
                'buenos', 'transformados', 'desechados'), (
                ))
        }),)


class Equipo_Devuelto_Inline(admin.StackedInline):
    model = Equipo_Devuelto
    extra = 0
    raw_id_fields = ('id_equipo',)
    #  Crea un campo de busqueda y debe poseer un search_fields
    #  en el modelo inicial para poder referenciar por esos campos
    autocomplete_fields = ['id_equipo']
    fieldsets = (
        (None, {
            'fields': ((
                'id_equipo', 'estado', 'comentarios',), (
                ))
        }),)


class AdminDevolucion(admin.ModelAdmin):
    inlines = [Material_DevueltoInline, Equipo_Devuelto_Inline]
    readonly_fields = ['create_by', 'id_no', 'fecha', 'hora', 'assigned_to']
    fieldsets = (
        (None, {
            'fields': (('id_no', 'create_by', 'fecha', 'hora'), (
                'assigned_to', 'asig_id'))
        }),
        ('Agregar Comentario', {
            'classes': ('collapse',),
            'fields': ('comentario',)
            })
        )
    list_display = [
        'id_no', 'create_by', 'fecha',
        'hora', 'assigned_to', 'estado_color', 'monto_total', 'detalle_dev']
    search_fields = ['id_no']
    list_filter = ['create_by', 'fecha']
    raw_id_fields = ['asig_id']
    list_display_links = ('id_no', )
    actions = ['disponible_update']

    def get_queryset(self, request, *args, **kwargs):
        ''' -- Funcion que se encarga de filtar el contenido
        en de que usuario sea igual al usuario logeado -- '''
        qs = super(AdminDevolucion, self).get_queryset(
            request, *args, **kwargs)
        log_perfil = Perfil.objects.filter(user=request.user).get()
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Administradores').exists():
            return qs
        else:
            return qs.filter(create_by=log_perfil)

    # Funcion para que la fk author seleccione al usuario logueado
    def save_model(self, request, obj, form, change):
        ''' trabajamos sobre el usuario logeado '''
        re_user = request.user
        perfil = Perfil.objects.filter(user=re_user).get()
        ''' ahora trabajamos sobre el perfil del administrador '''
        users = User.objects.all()
        admin = None
        for user in users:
            if user.groups.filter(name='Administradores'):
                admin = user
        perfil_admin = Perfil.objects.filter(user=admin).get()
        obj.assigned_to = perfil_admin
        obj .create_by = perfil
        super().save_model(request, obj, form, change)


class AdminRecepccion(admin.ModelAdmin):
    inlines = [Material_DevueltoInline, Equipo_Devuelto_Inline]
    readonly_fields = ['create_by', 'id_no', 'fecha', 'hora', 'assigned_to']
    fieldsets = (
        (None, {
            'fields': (('id_no', 'create_by', 'fecha', 'hora'), (
                'assigned_to', 'asig_id'))
        }),)
    list_display = [
        'id_no', 'create_by', 'fecha',
        'hora', 'assigned_to', 'estado_color', 'monto_total', 'detalle_dev']
    search_fields = ['id_no']
    list_filter = ['create_by', 'fecha']
    raw_id_fields = ['asig_id']
    list_display_links = ('id_no', )
    actions = ['aceptar_devolucion']

    def aceptar_devolucion(self, request, queryset, *args, **kwargs):
        ''' -- Funcion que se encarga modificar y aceptar las asignaciones
        que le ha realizado el administrador de bodega -- '''
        log_perfil = Perfil.objects.filter(user=request.user).get()
        qs = super(AdminRecepccion, self).get_queryset(
            request, *args, **kwargs)
        if qs.filter(assigned_to=log_perfil):
            pass
            for row in queryset.filter(estado=False):
                self.log_change(request, row, 'Aceptar Devolucion')
            rows_updated = 0

            for obj in queryset:
                if not obj.estado:
                    obj.estado = True
                    obj.save()

                    rows_updated += 1

            if rows_updated == 1:
                message_bit = 'Se aceptado una Devolucion'
            else:
                message_bit = '%s Devolucion fueno aceptadas' % rows_updated
            self.message_user(
                request, '%s satisfactoriamente como aceptadas' % message_bit)
        else:
            self.message_user(
                request, format_html(
                    '<span class="icon-error_outline"'
                    'style="color: black; font-weight: bold;'
                    'text-shadow: 0px 0px 2px #FF0220; '
                    'padding-right: 10px; font-size:22px;"></span>'
                    '<span style="color: black; font-weight: bold;'
                    'text-shadow: 0px 0px 2px #FF0220;'
                    'text-transform: uppercase; font-size:22px;">'
                    'Solamente pueden ser aceptadas por la persona'
                    'a quien se asigno</span>'))
    aceptar_devolucion.short_description = 'Aceptar Devolucion'

admin.site.register(Asignacion, AdminAsignacion)
admin.site.register(Devolucion, AdminDevolucion)
# admin.site.register(Material_Asignado, AdminMaterial_Asignado)
admin.site.register(Recepccion, AdminRecepccion)

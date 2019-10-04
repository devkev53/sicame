from django.contrib import admin
from .models import *

# Register your models here.


class Admin_Marca(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']

admin.site.register(Marca, Admin_Marca)
admin.site.register(Categoria)

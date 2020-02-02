from django.contrib import admin
from django.contrib import messages
from .models import *

# Register your models here.


# Clase que permite modificar la repsesentacion del modelo en el admin
class Admin_Marca(admin.ModelAdmin):
    # Agrega un buscador al modelo, segun los campos que se indiquen
    search_fields = ['nombre']
    # Ordena las instancias segun los campos que se indiquen
    ordering = ['nombre']

    '''def save_model(self, rquest, obj, form, change):
                    messages.add_message(rquest, messages.INFO, 'Karlo se la come')
                    super(Admin_Marca, self).save_model(rquest, obj, form, change)'''

admin.site.register(Marca, Admin_Marca)
admin.site.register(Categoria)

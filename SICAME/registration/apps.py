from django.apps import AppConfig
# con HTML una variable o texto para poder mostrar en el admin*'''
from django.utils.html import format_html


class RegistrationConfig(AppConfig):
    alias = ''
    name = 'registration'
    verbose_name = 'Perfiles'

default_app_config = 'registrarion.apps.RegistrationConfig'

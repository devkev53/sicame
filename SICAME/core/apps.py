from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Catergorias y Marcas'

default_app_config = 'core.apps.CoreConfig'

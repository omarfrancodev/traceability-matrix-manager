from django.apps import AppConfig


class CustompermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custompermissions'
    
    def ready(self):
        from . import signals
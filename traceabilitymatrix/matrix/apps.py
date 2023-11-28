from django.apps import AppConfig


class MatrixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matrix'
    
    def ready(self):
        from . import signals

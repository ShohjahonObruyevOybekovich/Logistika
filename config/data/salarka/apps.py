from django.apps import AppConfig


class SalarkaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data.salarka'
    def ready(self):
        import data.salarka.signals
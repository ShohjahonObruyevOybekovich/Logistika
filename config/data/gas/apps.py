from django.apps import AppConfig


class GasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "data.gas"
    
    def ready(self):
        import data.gas.signals

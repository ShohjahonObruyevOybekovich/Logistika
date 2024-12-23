from django.apps import AppConfig


class OilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data.oil'
    def ready(self):
        import data.oil.signals

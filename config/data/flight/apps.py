from django.apps import AppConfig


class FlightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data.flight'

    def ready(self):
        import data.flight.signals
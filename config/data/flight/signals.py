from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Flight, Ordered
from ..finans.models import Logs


@receiver(post_save, sender=Flight)
def handle_flight_completion(sender, instance: Flight, created, **kwargs):
    if created:
        if instance.status == "COMPLETED":
            # Log income for the flight
            if instance.price_uzs > 0:
                Logs.objects.create(
                    action="INCOME",
                    amount_uzs=instance.price_uzs,
                    # amount_usd=instance.price_usd,
                    kind="FLIGHT",
                    comment=f"Income from flight ID {instance}",
                    flight=instance,
                    employee=instance.driver,
                )

            # Log outcome for the flight
            if instance.driver_expenses_uzs > 0:
                Logs.objects.create(
                    action="OUTCOME",
                    amount_uzs=instance.driver_expenses_uzs,
                    # amount_usd=instance.driver_expenses_usd,
                    kind="FLIGHT",
                    comment=f"Outcome for flight ID {instance}",
                    flight=instance,
                    employee=instance.driver,
                )




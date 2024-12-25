from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Flight
from ..finans.models import Logs


@receiver(post_save, sender=Flight)
def handle_flight_status_update(sender, instance: Flight, created, **kwargs):
    # The signal should only work during updates (not creation)
    if created:
        return

    if instance.status == "INACTIVE":
        try:
            with transaction.atomic():
                # Log income if applicable
                if instance.price_uzs > 0:
                    Logs.objects.create(
                        action="INCOME",
                        amount_uzs=instance.price_uzs,
                        kind="FLIGHT",
                        comment=f"Income from flight ID {instance}",
                        flight=instance,
                        employee=instance.driver,
                    )

                # Log outcome for driver expenses
                if instance.driver_expenses_uzs > 0:
                    Logs.objects.create(
                        action="OUTCOME",
                        amount_uzs=instance.driver_expenses_uzs,
                        kind="FLIGHT",
                        comment=f"Outcome for flight ID {instance}",
                        flight=instance,
                        employee=instance.driver,
                    )

                # Update driver balance
                if instance.driver:
                    instance.driver.balance_uzs += instance.driver_expenses_uzs
                    instance.driver.save()

        except Exception as e:
            # Log error or handle as needed
            print(f"Error handling flight status update signal: {e}")

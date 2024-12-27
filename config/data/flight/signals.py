from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Flight, Ordered
from ..finans.models import Logs


@receiver(post_save, sender=Flight)
def handle_flight_status_update(sender, instance: Flight, created, **kwargs):
    if created:

        if instance.price_uzs > 0:
            Logs.objects.create(
                action="INCOME",
                amount_uzs=instance.price_uzs,
                kind="FLIGHT",
                comment=f"Доход от рейса с ID {instance.departure_date}.",
                flight=instance,
                employee=instance.driver,
            )

        # Log outcome for driver expenses
        if instance.driver_expenses_uzs > 0:
            Logs.objects.create(
                action="OUTCOME",
                amount_uzs=instance.driver_expenses_uzs,
                kind="FLIGHT",
                comment=f"Расход на рейс с ID {instance.departure_date}.",
                flight=instance,
                employee=instance.driver,
            )
        if instance.other_expences:
            Logs.objects.create(
                action="OUTCOME",
                amount_uzs=instance.other_expences,
                kind="FLIGHT",
                comment=f"Расход за рейс для водителя {instance.driver.full_name}: {instance.other_expences} ",
            )
            instance.driver.balance_uzs += float(instance.other_expences)
            instance.driver.save()


        # Update driver balance
        if instance.driver:
            instance.driver.balance_uzs += instance.driver_expenses_uzs
            instance.driver.save()


@receiver(post_save, sender=Ordered)
def handle_ordered_status_update(sender, instance: Ordered, created, **kwargs):
    # The signal should only work during updates (not creation)
    if created:
        # if instance.status == "INACTIVE":
            try:
                with transaction.atomic():
                    # Log income if applicable
                    if instance.price_uzs > 0:
                        Logs.objects.create(
                            action="INCOME",
                            amount_uzs=instance.price_uzs,
                            kind="ORDERED_FLIGHT",
                            comment=f"Доход от заказанного рейса (ID) {instance}",
                            flight=instance,
                        )

                    if instance.driver_expenses_uzs > 0:
                        Logs.objects.create(
                            action="OUTCOME",
                            amount_uzs=instance.driver_expenses_uzs,
                            kind="ORDERED_FLIGHT",
                            comment=f"Доход от заказанного рейса  {instance.driver_name}"
                        )


            except Exception as e:
                # Log error or handle as needed
                print(f"Error handling ordered flight status update signal: {e}")


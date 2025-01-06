from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Car, Notification, Details
from ..finans.models import Logs


@receiver(post_save, sender=Car)
def send_oil_recycle_notification(sender, instance, **kwargs):
    if instance.check_oil_recycle_notification():
        # Send a notification
        # You can use any notification mechanism here (e.g., email, push, or database notification)
        print(f"Уведомление: Автомобиль {instance.name} приближается к следующему пробегу для замены масла.")


@receiver(post_save, sender=Car)
def send_oil_recycle_notification(sender, instance:Car, **kwargs):
    if instance.check_oil_recycle_notification():
        # Example: Save the notification to the database
        Notification.objects.create(
            message=f"Автомобиль с номером {instance.number} приближается к следующему пробегу для замены масла."
        )

@receiver(post_save, sender=Car)
def on_car_create(sender, instance: Car, created, **kwargs):
    if created and instance.type_of_payment=="CASH":
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.price_uzs,
            amount=instance.price,
            amount_type=instance.price_type,
            kind="OTHER",
            comment=f"За покупку техники / {instance.name} и {instance.number} "
        )

@receiver(post_save, sender=Details)
def on_details_create(sender, instance: Details, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.price_uzs,
            amount=instance.price,
            amount_type=instance.price_type,
            car=instance.car,
            kind="OTHER",
            comment=f"Детали для машины {instance.car.name}-{instance.car.number} обновлены."
        )
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Car, Notification


@receiver(post_save, sender=Car)
def send_oil_recycle_notification(sender, instance, **kwargs):
    if instance.check_oil_recycle_notification():
        # Send a notification
        # You can use any notification mechanism here (e.g., email, push, or database notification)
        print(f"Notification: Car {instance.name} is nearing the next oil recycle distance.")


@receiver(post_save, sender=Car)
def send_oil_recycle_notification(sender, instance:Car, **kwargs):
    if instance.check_oil_recycle_notification():
        # Example: Save the notification to the database
        Notification.objects.create(
            message=f"Car {instance.number} is nearing the next oil recycle distance."
        )

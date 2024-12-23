from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flight


@receiver(post_save, sender=Flight)
def on_oil_purchased(sender, instance: Flight, created, **kwargs):
    if created:
        pass



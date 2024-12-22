from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GasPurchase


@receiver(post_save, sender=GasPurchase)
def on_gas_purchased(sender, instance: GasPurchase, created, **kwargs):
    if created:

        instance.station.remaining_gas += instance.amount
        instance.station.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Salarka, Remaining_volume, Sale


@receiver(post_save, sender=Salarka)
def on_oil_purchased(sender, instance: Salarka, created, **kwargs):
    remaining_volume = Remaining_volume.volume
    if created:
        remaining_volume += instance.volume
        instance.volume.save()


@receiver(post_save, sender=Sale)
def on_sale_purchased(sender, instance: Sale, created, **kwargs):
    remaining_volume = Remaining_volume.volume
    if created:
        remaining_volume -= instance.volume
        remaining_volume.save()

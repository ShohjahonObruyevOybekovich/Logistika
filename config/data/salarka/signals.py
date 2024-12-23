from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Salarka , Remaining_volume

@receiver(post_save, sender=Salarka)
def on_oil_purchased(sender, instance: Salarka, created, **kwargs):
    if created:
        instance.volume += Salarka
        instance.volume.save()


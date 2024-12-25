from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Salarka, Remaining_volume, Sale
from ..finans.models import Logs


@receiver(post_save, sender=Salarka)
def on_oil_purchased(sender, instance: Salarka, created, **kwargs):
    if created:
        remaining_volume = Remaining_volume.objects.first()
        if remaining_volume:

            remaining_volume.volume += instance.volume
            remaining_volume.save()



@receiver(post_save, sender=Sale)
def on_sale_purchased(sender, instance: Sale, created, **kwargs):
    if created:
        remaining_volume = Remaining_volume.objects.first()  # Get the instance of Remaining_volume
        if remaining_volume:
            remaining_volume.volume -= instance.volume
            remaining_volume.save()


# INcome
@receiver(post_save, sender=Salarka)
def income(sender, instance: Salarka, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.price_uzs,
            # amount_usd=instance.price_usd,
            kind="OTHER",
            comment=f"За {instance.price_uzs} сум была закуплена солярка."
        )

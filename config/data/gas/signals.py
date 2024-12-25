from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GasPurchase, GasSale
from ..finans.models import Logs
from ..oil.models import Utilized_oil


@receiver(post_save, sender=GasPurchase)
def on_gas_purchased(sender, instance: GasPurchase, created, **kwargs):
    if created:

        instance.station.remaining_gas += instance.amount
        instance.station.save()


@receiver(post_save, sender=GasSale)
def on_gas_sold(sender, instance: GasSale, created, **kwargs):

    if created:

        instance.station.remaining_gas -= instance.amount
        instance.station.save()

@receiver(post_save, sender=GasPurchase)
def income(sender, instance: GasPurchase, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.price_uzs,
            # amount_usd=instance.price_usd,
            kind="OTHER",
            comment=f"{instance.station} Газ был закуплен",
        )



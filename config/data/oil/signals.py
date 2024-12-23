from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OilPurchase, OilREcycles, Utilized_oil, Remaining_oil_quantity


@receiver(post_save, sender=OilPurchase)
def on_oil_purchased(sender, instance: OilPurchase, created, **kwargs):
    if created:
        instance.oil.oil_volume += instance.oil_volume
        instance.oil.save()


@receiver(post_save, sender=OilREcycles)
def on_oil_recycled(sender, instance: OilREcycles, created, **kwargs):
    if created:
        instance.oil.oil_volume -= instance.remaining_oil
        instance.oil.save()


@receiver(post_save, sender=OilREcycles)
def oil_recycled(sender, instance: OilREcycles, created, **kwargs):
    recycle = Remaining_oil_quantity.get()
    if created:
        instance.remaining_oil += recycle.oil_volume
        instance.save()


@receiver(post_save, sender=Utilized_oil)
def on_utilized(sender, instance: Utilized_oil, created, **kwargs):
    recycle = Remaining_oil_quantity.get()

    if created:
        recycle.oil_volume -= (
            instance.quantity_utilized)
        recycle.save()

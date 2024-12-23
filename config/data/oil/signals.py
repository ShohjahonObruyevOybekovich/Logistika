from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OilPurchase, OilREcycles, Utilized_oil, Remaining_oil_quantity


@receiver(post_save, sender=OilPurchase)
def on_oil_purchased(sender, instance: OilPurchase, created, **kwargs):
    if created:
        # Update Oil volume
        instance.oil.oil_volume += instance.oil_volume
        instance.oil.save()

        print(instance.oil.oil_volume)

        remaining_oil = Remaining_oil_quantity.get()
        remaining_oil.oil_volume += instance.oil_volume
        remaining_oil.save()
        print(remaining_oil.oil_volume)


@receiver(post_save, sender=OilREcycles)
def on_oil_recycled(sender, instance: OilREcycles, created, **kwargs):
    if created:

        remaining_oil = Remaining_oil_quantity.get()
        remaining_oil.oil_volume -= instance.remaining_oil
        remaining_oil.save()

        utilized_oil = Utilized_oil.get()
        utilized_oil.quantity_utilized += instance.remaining_oil
        utilized_oil.save()


# @receiver(post_save, sender=Utilized_oil)
# def on_utilized(sender, instance: Utilized_oil, created, **kwargs):
#     if created:
#         # Deduct utilized oil quantity
#         remaining_oil = Remaining_oil_quantity.get()
#         remaining_oil.oil_volume -= instance.quantity_utilized
#         remaining_oil.save()



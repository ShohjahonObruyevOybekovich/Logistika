from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OilPurchase, OilREcycles, Utilized_oil, Remaining_oil_quantity
from ..finans.models import Logs


@receiver(post_save, sender=OilPurchase)
def on_oil_purchased(sender, instance: OilPurchase, created, **kwargs):
    if created:
        instance.oil.oil_volume += instance.oil_volume
        instance.oil.save()

        print(instance.oil.oil_volume)


@receiver(post_save, sender=OilREcycles)
def on_oil_recycled(sender, instance: OilREcycles, created, **kwargs):
    if created:
        #Moy miqdoridan ayirilib Jami maslaga qushildi

        instance.oil.oil_volume -= instance.remaining_oil
        instance.oil.save()

        remaining_oil = Remaining_oil_quantity.get()
        remaining_oil.oil_volume += instance.remaining_oil
        remaining_oil.save()


@receiver(post_save, sender=Utilized_oil)
def on_utilized(sender, instance: Utilized_oil, created, **kwargs):
    if created:
        # Deduct utilized oil quantity
        remaining_oil = Remaining_oil_quantity.get()
        remaining_oil.oil_volume -= instance.quantity_utilized
        remaining_oil.save()




# income
@receiver(post_save, sender=Utilized_oil)
def on_income(sender, instance: Utilized_oil, created, **kwargs):
    if created:
        Logs.objects.create(
            action="Income",
            amount_uzs=instance.price_uzs,
            # amount_usds=instance.price_usd,
            kind="OTHER",
            comment=f"{instance.price_uzs} $ доход от продажи {instance.quantity_utilized} литров переработанного масла",
        )


@receiver(post_save, sender=OilPurchase)
def on_purchase(sender, instance: OilPurchase, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.amount_uzs,
            # amount_usd=instance.amount_usd,
            kind="OTHER",
            comment=f"{instance.amount_uzs} $ расход для покупки {instance.oil_volume} литров масла {instance.oil.oil_name}"
        )



@receiver(post_save, sender=OilREcycles)
def on_recycled(sender, instance: OilREcycles, created, **kwargs):
    if created:
        # Ensure next_oil_recycle_distance is initialized
        if instance.car.next_oil_recycle_distance is None:
            instance.car.next_oil_recycle_distance = 0

        # Add oil_recycle_distance to next_oil_recycle_distance
        instance.car.next_oil_recycle_distance += instance.car.oil_recycle_distance

        instance.car.save()
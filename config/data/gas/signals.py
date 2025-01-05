from django.db.models.signals import post_save
from django.dispatch import receiver
from icecream import ic

from .models import GasPurchase, GasSale, Gas_another_station
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
            amount_uzs=instance.amount,
            # amount_usd=instance.price_usd,
            kind="OTHER",
            comment=f"{instance.station.name} Газ был закуплен",
        )


@receiver(post_save, sender=Gas_another_station)
def outcome(sender, instance: Gas_another_station, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.payed_price_uzs,
            amount=instance.payed_price,
            amount_type=instance.payed_price_type,
            car=instance.car,
            kind="OTHER",
            comment=f"Расход для покупки газа с других заправок {instance.name}."
        )

@receiver(post_save, sender=GasSale)
def sold(sender, instance: GasSale, created, **kwargs):
    if created:
        # Fetch gas purchases for the same car
        purchased_gas = GasSale.objects.filter(car__id=instance.car.id)
        purchased_another_station = Gas_another_station.objects.filter(car__id=instance.car.id)

        # Combine and sort by created_at
        combined_purchases = sorted(
            list(purchased_gas) + list(purchased_another_station),
            key=lambda x: x.created_at,
            reverse=True
        )

        # Get the last purchased gas
        last_purchased_gas = combined_purchases[0] if combined_purchases else None
        ic(last_purchased_gas)

        # Update the previous purchase's used_volume
        if len(combined_purchases) > 1:
            previous_purchase = combined_purchases[1]
            previous_purchase.used_volume = instance.amount
            previous_purchase.save()  # Save changes to the database

        # Update the current instance's km field
        if instance.car.distance_travelled is not None and instance.km_car is not None:
            instance.km = instance.car.distance_travelled - instance.km_car
            instance.save()


@receiver(post_save, sender=Gas_another_station)
def sold(sender, instance: Gas_another_station, created, **kwargs):
    if created:
        # Fetch gas purchases for the same car
        purchased_gas = GasSale.objects.filter(car__id=instance.car.id)
        purchased_another_station = Gas_another_station.objects.filter(car__id=instance.car.id)

        # Combine and sort by created_at
        combined_purchases = sorted(
            list(purchased_gas) + list(purchased_another_station),
            key=lambda x: x.created_at,
            reverse=True
        )

        # Get the last purchased gas
        last_purchased_gas = combined_purchases[0] if combined_purchases else None
        ic(last_purchased_gas)

        # Update the previous purchase's used_volume
        if len(combined_purchases) > 1:
            previous_purchase = combined_purchases[1]
            previous_purchase.used_volume = instance.purchased_volume
            previous_purchase.save()  # Save changes to the database

        # Update the current instance's km field
        if instance.car.distance_travelled is not None and instance.km_car is not None:
            instance.km = instance.car.distance_travelled - instance.km_car
            instance.save()
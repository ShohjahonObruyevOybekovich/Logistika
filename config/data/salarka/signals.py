from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Salarka, Remaining_volume, Sale, SalarkaAnotherStation
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


@receiver(post_save, sender=SalarkaAnotherStation)
def on_logs_another_purchased(sender, instance: SalarkaAnotherStation, created, **kwargs):
    if created:
        Logs.objects.create(
            action="OUTCOME",
            amount_uzs=instance.price_uzs,
            amount_type=instance.price_type,
            amount=instance.price,
            car=instance.car,
            kind="OTHER",
            comment=f"Продано {instance.volume} литр солярки за {instance.price} {instance.price_type}. Оплата произведена в {instance.price_type}."
        )

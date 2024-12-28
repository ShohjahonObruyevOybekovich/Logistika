from django.db import models

from data.command.models import TimeStampModel


class Salarka(TimeStampModel):
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT, help_text="Salarka car")
    volume = models.PositiveIntegerField(help_text="Volume of the car")
    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)


class Sale(TimeStampModel):
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT, help_text="Sale car")
    volume = models.PositiveIntegerField(help_text="Volume of the sale")


class Remaining_volume(TimeStampModel):
    volume = models.FloatField(max_length=150, help_text="Remaining volume")

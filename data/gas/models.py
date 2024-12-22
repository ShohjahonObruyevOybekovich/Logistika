from itertools import count

from django.db import models

from data.cars.models import Car
from data.command.models import TimeStampModel


class GasStation(TimeStampModel):

    name = models.CharField(max_length=100, help_text="Name of gas station")

    remaining_gas = models.FloatField()


class GasPurchase(TimeStampModel):

    station = models.ForeignKey("GasStation", on_delete=models.CASCADE, null=True)

    remaining_gas = models.FloatField(help_text="Volume of gas purchased in m³")

    payed_price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    payed_price_usd = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )

    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price_usd = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )

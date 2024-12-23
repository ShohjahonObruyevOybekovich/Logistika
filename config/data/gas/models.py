from itertools import count

from django.db import models

from data.command.models import TimeStampModel

from data.cars.models import Car


class GasStation(TimeStampModel):

    name = models.CharField(max_length=100, help_text="Name of gas station")

    remaining_gas = models.FloatField(default=0)

    purchases: "models.QuerySet[GasPurchase]"
    sales: "models.QuerySet[GasSale]"


class GasPurchase(TimeStampModel):

    station: "GasStation" = models.ForeignKey(
        "gas.GasStation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="purchases",
    )

    amount = models.FloatField(help_text="Volume of gas purchased in m³")

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


class GasSale(TimeStampModel):

    station: "GasStation" = models.ForeignKey(
        "gas.GasStation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sales",
    )

    car = models.ForeignKey(
        "cars.Car", on_delete=models.CASCADE, related_name="gas_sales"
    )

    amount = models.FloatField(help_text="Volume of gas purchased in m³")

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

class Gas_another_station(TimeStampModel):
    car: "Car" = models.ForeignKey("cars.Car", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Name of gas station")
    purchased_volume = models.FloatField(help_text="Volume of gas purchased in m³")
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

    def __str__(self):
        return f"Purchased {self.purchased_volume} gas - {self.payed_price_uzs} m³"


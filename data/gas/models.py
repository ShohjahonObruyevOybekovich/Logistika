from itertools import count

from django.db import models

from data.cars.models import Car
from data.command.models import TimeStampModel


# class GasStation(TimeStampModel):
#     name = models.CharField(max_length=100)
#     gas_volume = models.FloatField(default=0,help_text="Remaining gas volume in m³")
#     last_payment = models.DateField(auto_now=True,null=True, blank=True)
#     def __str__(self):
#         return f"Gas Inventory - {self.gas_volume} m³ remaining"


class Gas_another_station(TimeStampModel):
    car : Car = models.ForeignKey("cars.Car", on_delete=models.CASCADE)
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


from django.db.models import Sum

class GasPurchase(TimeStampModel):
    station = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
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

    def __str__(self):
        return f"Purchase from {self.station} - {self.purchased_volume} m³"

    @classmethod
    def get_totals(cls, pk):
        """
        Calculate the total gas purchased and total prices (UZS and USD) for a station.
        """
        totals = cls.objects.filter(id=pk).aggregate(
            total_volume=Sum('purchased_volume'),
            total_price_uzs=Sum('price_uzs'),
            total_price_usd=Sum('price_usd')
        )
        return {
            "total_volume": totals["total_volume"] or 0,
            "total_price_uzs": totals["total_price_uzs"] or 0,
            "total_price_usd": totals["total_price_usd"] or 0,
        }


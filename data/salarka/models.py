from django.db import models
from django.db.models import Sum

from data.command.models import  TimeStampModel


class Salarka(TimeStampModel):
    purchased_volume = models.CharField(max_length=100, help_text="Salarka volume litr")
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT,help_text="Salarka car")
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
        return self.purchased_volume

    @classmethod
    def get_totals(cls, car_id):
        """
        Calculate the total gas purchased and total prices (UZS and USD) for a station.
        """
        totals = cls.objects.filter(car_id=car_id).aggregate(
            total_volume=Sum('purchased_volume'),
            total_price_uzs=Sum('price_uzs'),
            total_price_usd=Sum('price_usd')
        )
        return {
            "total_volume": totals["total_volume"] or 0,
            "total_price_uzs": totals["total_price_uzs"] or 0,
            "total_price_usd": totals["total_price_usd"] or 0,
        }


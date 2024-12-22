from django.db import models
from data.command.models import  TimeStampModel


class Oil(TimeStampModel):
    oil_name = models.CharField(max_length=100, help_text="Oil name")
    oil_volume = models.CharField(max_length=100, help_text="Oil volume litr")
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
        return self.oil_name


class Remaining_oil_quantity(TimeStampModel):
    oil_volume = models.FloatField(max_length=100, help_text="Oil volume litr")


    def __str__(self):
        return self.oil_volume


class Recycled_oil(TimeStampModel):
    oil_volume = models.FloatField(max_length=100, help_text="Oil volume litr")

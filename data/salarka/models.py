from django.db import models
from data.command.models import  TimeStampModel


class Salarka(TimeStampModel):
    oil_volume = models.CharField(max_length=100, help_text="Salarka volume litr")
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
        return self.oil_volume


class Remaining_salarka_quantity(TimeStampModel):
    oil_volume = models.CharField(max_length=100, help_text="Salarka volume litr")

    def __str__(self):
        return self.oil_volume



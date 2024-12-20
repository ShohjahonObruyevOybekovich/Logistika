from django.db import models
from data.command.models import  TimeStampModel


class Salarka(TimeStampModel):
    oil_volume = models.CharField(max_length=100, help_text="Salarka volume litr")
    oil_price = models.CharField(max_length=100, help_text="Salarka price")

    def __str__(self):
        return self.oil_volume


class Remaining_gas_quantity(TimeStampModel):
    oil_volume = models.CharField(max_length=100, help_text="Salarka volume litr")

    def __str__(self):
        return self.oil_volume



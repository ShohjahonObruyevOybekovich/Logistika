from django.db import models
from data.command.models import  TimeStampModel


class Oil(TimeStampModel):
    oil_name = models.CharField(max_length=100, help_text="Oil name")
    oil_volume = models.CharField(max_length=100, help_text="Oil volume litr")
    paid_amount = models.CharField(max_length=100, help_text="Oil paid amount")
    oil_price = models.CharField(max_length=100, help_text="Oil price")


    def __str__(self):
        return self.oil_name


class Remaining_oil_quantity(TimeStampModel):
    oil_volume = models.CharField(max_length=100, help_text="Oil volume litr")


    def __str__(self):
        return self.oil_volume



from itertools import count

from django.db import models
from data.command.models import TimeStampModel


class GasStation(TimeStampModel):
    name = models.CharField(max_length=100)
    gas_volume = models.FloatField(default=0,help_text="Remaining gas volume in m³")
    last_payment = models.DateField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return f"Gas Inventory - {self.gas_volume} m³ remaining"


class Gas_another_station(TimeStampModel):
    purchased_volume = models.FloatField(help_text="Volume of gas purchased in m³")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                      help_text="Amount paid for the gas")

    def __str__(self):
        return f"Purchased {self.purchased_volume} gas - {self.paid_amount} m³"


class GasPurchase(TimeStampModel):
    station :GasStation = models.ForeignKey("GasStation", on_delete=models.CASCADE)
    purchased_volume = models.FloatField(help_text="Volume of gas purchased in m³")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                      help_text="Amount paid for the gas")
    gas_price = models.DecimalField(max_digits=10, decimal_places=2,
                                    help_text="Price per m³ of gas")

    def __str__(self):
        return f"Purchase from {self.station} - {self.purchased_volume} m³"


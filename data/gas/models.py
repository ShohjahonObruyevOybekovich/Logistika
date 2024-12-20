from django.db import models
from data.command.models import TimeStampModel


class GasInventory(TimeStampModel):
    remaining_gas_volume = models.FloatField(default=0,
                                             help_text="Remaining gas volume in m³")
    remaining_payment = models.DecimalField(max_digits=12, decimal_places=1,
                                            help_text="Remaining payment in currency")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gas Inventory - {self.remaining_gas_volume} m³ remaining"

class Gas_another_station(TimeStampModel):
    purchased_volume = models.FloatField(help_text="Volume of gas purchased in m³")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                      help_text="Amount paid for the gas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchased {self.purchased_volume} gas - {self.paid_amount} m³"


class GasPurchase(TimeStampModel):
    purchased_volume = models.FloatField(help_text="Volume of gas purchased in m³")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                      help_text="Amount paid for the gas")
    gas_price = models.DecimalField(max_digits=10, decimal_places=2,
                                    help_text="Price per m³ of gas")
    station_name = models.CharField(max_length=255,
                                    help_text="Name of the gas station")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Purchase from {self.station_name} - {self.purchased_volume} m³"


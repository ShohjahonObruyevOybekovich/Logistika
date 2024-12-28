from django.db import models

from data.command.models import TimeStampModel


class Salarka(TimeStampModel):
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT, help_text="Salarka car")
    volume = models.PositiveIntegerField(help_text="Volume of the car")
    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.car.name} ({self.volume})"


class Sale(TimeStampModel):
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT, help_text="Sale car")
    volume = models.PositiveIntegerField(help_text="Volume of the sale")
    km = models.FloatField(default=0.0, help_text="Kilometer Miles",null=True, blank=True)
    km_car = models.FloatField(default=0.0, help_text="Kilometer Miles",null=True, blank=True)

    def __str__(self):
        return f"{self.car.name} ({self.volume})"


class Remaining_volume(TimeStampModel):
    volume = models.FloatField(max_length=150,default=0, help_text="Remaining volume")
    def __str__(self):
        return f"{self.volume}"


class SalarkaAnotherStation(TimeStampModel):
    car = models.ForeignKey("cars.Car", on_delete=models.PROTECT, help_text="Sale car")
    flight = models.ForeignKey(
        "flight.Flight", on_delete=models.SET_NULL, null=True, blank=True
    )
    volume = models.PositiveIntegerField(help_text="Volume of the sale")
    price = models.FloatField(max_length=150, help_text="Price of the sale",null=True,blank=True)
    price_uzs = models.FloatField(max_length=150,null=True,blank=True)
    price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.car.name} - {self.flight.region.name})"

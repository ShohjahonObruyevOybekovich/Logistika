from django.db import models
from data.command.models import TimeStampModel
from account.models import CustomUser

class Car(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of car')
    driver = models.ForeignKey(CustomUser, on_delete=models.PROTECT, help_text='Driver user')
    number = models.CharField(max_length=10, help_text='Number of car')
    model_car = models.CharField(max_length=30, help_text='Model car')
    TYPE_OF_PAYMENT_CHOICES = [
        ("lizing", "Lizing"),
        ("nalichi", "Nalichi"),
    ]

    type_of_payment = models.CharField(
        max_length=30,
        choices=TYPE_OF_PAYMENT_CHOICES,
        default="lizing",
        help_text="Type of payment"
    )
    lizing_period = models.CharField(max_length=155,help_text='Lizing period',
                                     null=True,blank=True)
    with_trailer = models.BooleanField(default=False, help_text='With trailer')
    FUEL_CHOICES = [
        ('Diesel', 'DIESEL'),
        ('Gas', 'GAS'),
    ]

    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_CHOICES,
        default='Diesel',
    )
    car_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    distance_travelled = models.IntegerField(
        default=0,
        help_text="The distance the car has traveled in kilometers"
    )

    def has_trailer(self):
        """Check if the car has a trailer."""
        return self.with_trailer

    def __str__(self):
        return f"{self.name} - {self.model_car} ({self.number})"


class Trailer_cars(TimeStampModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    trailer_number = models.CharField(max_length=10, help_text='Trailer number')

    def __str__(self):
        return f"Trailer {self.trailer_number} for Car {self.car.name}"

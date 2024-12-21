from django.db import models
from data.command.models import TimeStampModel
from employee.models import Employee



class Car(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of car')
    number = models.CharField(max_length=10, help_text='Number of car')
    model = models.CharField(max_length=30, help_text='Model car')
    TYPE_OF_PAYMENT_CHOICES = [
        ("LEASING", "Leasing"),
        ("CASH", "Cash"),
    ]

    type_of_payment = models.CharField(
        max_length=30,
        choices=TYPE_OF_PAYMENT_CHOICES,
        default="LEASING",
        help_text="Type of payment"
    )
    leasing_period = models.IntegerField(help_text='Leasing period',
                                     null=True,blank=True)
    with_trailer = models.BooleanField(default=False, help_text='With trailer')
    FUEL_CHOICES = [
        ('DIESEL','Diesel'),
        ('GAS','Gas'),
    ]

    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_CHOICES,
        default='Diesel',
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
    distance_travelled = models.IntegerField(
        default=0,
        help_text="The distance the car has traveled in kilometers"
    )
    trailer_number = models.CharField(max_length=10, help_text='Trailer number',
                                      null=True,blank=True)

    def __str__(self):
        return f"{self.name} - {self.model} ({self.number})"



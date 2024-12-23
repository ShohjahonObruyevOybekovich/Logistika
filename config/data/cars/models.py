from django.db import models
from data.command.models import TimeStampModel
from employee.models import Employee

class Model(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Car(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of car')
    number = models.CharField(max_length=10, help_text='Number of car')
    model = models.ForeignKey("Model", on_delete=models.CASCADE)
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


class Details(TimeStampModel):
    car  = models.ForeignKey("Car", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    id_detail = models.CharField(max_length=100,null=True,blank=True)
    price_uzs = models.DecimalField(decimal_places=2, max_digits=10,null=True,blank=True)
    price_usd = models.DecimalField(decimal_places=2, max_digits=10,null=True,blank=True)

    def __str__(self):
        return self.name

from django.db import models
from data.command.models import TimeStampModel
from employee.models import Employee


class Car(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of car')
    driver = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Driver user',
    )
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
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    distance_travelled = models.IntegerField(
        default=0,
        help_text="The distance the car has traveled in kilometers"
    )


    def __str__(self):
        return f"{self.name} - {self.model} ({self.number})"

    def get_last_used_driver(self):
        """Fetch the last used driver."""
        # Assuming you have a Car model with a 'driver' field, which is a ForeignKey to Employee
        last_car = Car.objects.order_by('-updated_at').first()
        return last_car.driver if last_car else None

class Trailer(TimeStampModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, help_text='Trailer number')

    def __str__(self):
        return f"Trailer {self.number} for Car {self.car.name}"

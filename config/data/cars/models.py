from django.contrib.auth import get_user_model
from django.db import models

from data.command.models import TimeStampModel

User = get_user_model()

class Model(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of car')
    number = models.CharField(max_length=100, help_text='Number of car')
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
                                         null=True, blank=True)

    leasing_payed_amount = models.FloatField(help_text='Leasing payment amount',null=True,blank=True)

    with_trailer = models.BooleanField(default=False, help_text='With trailer')
    FUEL_CHOICES = [
        ('DIESEL', 'Diesel'),
        ('GAS', 'Gas'),
    ]

    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_CHOICES,
        default='Diesel',
    )
    price = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    PRICE_CHOICES = [
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT"),
        ("UZS", "UZS"),
    ]
    price_type = models.CharField(
        choices=PRICE_CHOICES,
        default='USD',
        max_length=10,
        help_text="Type of price"
    )
    distance_travelled = models.FloatField(
        default=0,
        help_text="The distance the car has traveled in kilometers"
    )
    oil_recycle_distance = models.FloatField(
        default=0,
        help_text="The oil recycle distance in kilometers",
        null=True,
        blank=True,
    )
    next_oil_recycle_distance = models.FloatField(
        default=0,
        help_text="Next oil recycle distance",
        null=True,
        blank=True
    )
    trailer_number = models.CharField(max_length=100,
                                      help_text='Trailer number',
                                      null=True, blank=True)

    first_distance_travelled = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.model} ({self.number})"


    def check_oil_recycle_notification(self):
        """Check if the car is nearing the next oil recycle distance."""
        threshold = 50  # Define a threshold distance (e.g., 50 km)
        if self.next_oil_recycle_distance - self.distance_travelled <= threshold:
            return True
        return False
    def save(self, *args, **kwargs):

        self.first_distance_travelled = self.distance_travelled
        super().save(*args, **kwargs)



class Details(TimeStampModel):
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    id_detail = models.CharField(max_length=100, null=True, blank=True)
    price_uzs = models.FloatField(max_length=100, null=True, blank=True)
    price = models.FloatField(max_length=100, null=True, blank=True)
    PRICE_CHOICES = [
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT"),
        ("UZS", "UZS"),
    ]
    price_type = models.CharField(
        choices=PRICE_CHOICES,
        default='USD',
        max_length=10,
        help_text="Type of price"
    )
    in_sklad = models.BooleanField(default=False, help_text='In Sklad',null=True,blank=True)

    # price_usd = models.DecimalField(decimal_places=2, max_digits=10,null=True,blank=True)

    def __str__(self):
        return self.name or "Unnamed detail"



class Notification(TimeStampModel):
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for: {self.message}"

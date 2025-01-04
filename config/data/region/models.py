from django.db import models

from data.command.models import TimeStampModel


class Region(TimeStampModel):
    name = models.CharField(max_length=100, help_text="Name of the region")
    Flight_CHOICES = [
        ("IN_UZB", "In_uzb"),
        ("OUT", "Out"),
    ]

    flight_type = models.CharField(
        max_length=10,
        choices=Flight_CHOICES,
        default="IN_UZB",
    )

    flight_price = models.FloatField(
        null=True,
        blank=True,
    )
    flight_price_uzs= models.FloatField(
        null=True,
        blank=True,
    )
    flight_price_type= models.CharField(choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT"),
        ("UZS", "UZS"),
    ],default='USD', max_length=10, null=True, blank=True)
    driver_expenses= models.FloatField(
        null=True,
        blank=True,
    )
    driver_expenses_uzs= models.FloatField(
        null=True,
        blank=True,
    )
    driver_expenses_type= models.CharField(choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB'),
        ('KZT', "KZT"),
        ("UZS", "UZS"),
    ],default='USD', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

import datetime
from typing import TYPE_CHECKING

from django.db import models
from django.db import models
    # from data.flight.models import flight


class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    passport = models.CharField(max_length=20, help_text="Passport number",
                                null=True,blank=True)
    license = models.CharField(max_length=20, help_text="Prava number",
                               null=True,blank=True)
    Flight_CHOICES = [
        ('IN_UZB', 'In_uzb'),
        ('OUT', 'Out'),
    ]
    flight_type = models.CharField(
        max_length=10,
        choices=Flight_CHOICES,
        default='IN_UZB',
    )
    balance = models.DecimalField(max_digits=10, decimal_places=5,
                                  null=True,blank=True)

    created_at = models.DateField(auto_now_add=True,
                                  null=True, blank=True)
    updated_at = models.DateField(auto_now=True,
                                  null=True, blank=True)

    def __str__(self):
        return self.phone


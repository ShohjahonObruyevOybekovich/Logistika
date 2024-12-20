import datetime
from typing import TYPE_CHECKING

from django.db import models
from django.db import models
from account.managers import UserManager
from account.models import CustomUser

if TYPE_CHECKING:
    from data.city.models import City
    # from data.flight.models import flight


class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city: "City" = models.ForeignKey('city.city', on_delete=models.SET_NULL, null=True)
    price_of_flight = models.DecimalField(decimal_places=2, max_digits=10)
    # flight = models.ForeignKey('data.flight.flight', on_delete=models.SET_NULL, null=True)
    departure_date = models.DateField(auto_now=True,help_text="Enter the departure date")
    cargo_description = models.TextField(null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.phone


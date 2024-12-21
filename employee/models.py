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
    passport = models.CharField(max_length=20, help_text="Passport number")
    license = models.CharField(max_length=20, help_text="Prava number")
    flight = models.ForeignKey('flight.flight', on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=5)

    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.phone


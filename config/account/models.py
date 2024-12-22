from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import UserManager

if TYPE_CHECKING:
    from data.city.models import City
    # from data.flight.models import flight


class CustomUser(AbstractUser):
    username = None
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return self.full_name or self.phone





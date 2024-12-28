from django.db import models
from data.upload.models import File

# from data.flight.models import flight

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    passport = models.CharField(max_length=20, help_text="Passport number",
                                null=True, blank=True)
    passport_photo = models.ForeignKey(
        "upload.File",
        on_delete=models.SET_NULL,
        related_name="passport_employees",  # Unique related_name
        null=True,
        blank=True,
    )
    license = models.CharField(max_length=20, help_text="Prava number",
                               null=True, blank=True)
    license_photo = models.ForeignKey(
        "upload.File",
        on_delete=models.SET_NULL,
        related_name="license_employees",  # Unique related_name
        null=True,
        blank=True,
    )

    Flight_CHOICES = [
        ('IN_UZB', 'In_uzb'),
        ('OUT', 'Out'),
    ]
    flight_type = models.CharField(
        max_length=10,
        choices=Flight_CHOICES,
        default='IN_UZB',
    )
    balance_uzs = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    balance_price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ], default='USD', max_length=10, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True,
                                  null=True, blank=True)
    updated_at = models.DateField(auto_now=True,
                                  null=True, blank=True)

    def __str__(self):
        return self.phone

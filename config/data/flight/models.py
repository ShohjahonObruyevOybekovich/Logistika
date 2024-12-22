from django.db import models


from typing import TYPE_CHECKING


if TYPE_CHECKING:

    from config.data.cars.models import Car
    from config.data.city.models import Region
    from config.employee.models import Employee


class Flight(models.Model):
    region: "Region" = models.ForeignKey(
        "city.Region", on_delete=models.CASCADE, related_name="flights"
    )

    Flight_CHOICES = [
        ("IN_UZB", "In_uzb"),
        ("OUT", "Out"),
    ]

    flight_type = models.CharField(
        max_length=10,
        choices=Flight_CHOICES,
        default="IN_UZB",
    )

    car: "Car" = models.ForeignKey(
        "cars.Car", on_delete=models.CASCADE, related_name="flights"
    )
    driver: "Employee" = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE, related_name="flights"
    )

    departure_date = models.DateField()
    arrival_date = models.DateField(null=True, blank=True)

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

    driver_expenses_uzs = models.FloatField(
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )

    driver_expenses_usd = models.FloatField(
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )

    cargo_info = models.TextField(blank=True, null=True)

    upload = models.ForeignKey(
        "upload.File",
        on_delete=models.CASCADE,
        related_name="flights",
        null=True,
        blank=True,
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )
    status = models.BooleanField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active",
    )

    def __str__(self):
        return f"Flight - {self.route} ({self.departure_date})"

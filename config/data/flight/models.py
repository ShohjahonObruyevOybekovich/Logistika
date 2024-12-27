from typing import TYPE_CHECKING

from django.db import models

from data.command.models import TimeStampModel

if TYPE_CHECKING:
    from data.cars.models import Car
    from data.region.models import Region
    from employee.models import Employee


class Flight(TimeStampModel):
    region: "Region" = models.ForeignKey(
        "region.Region", on_delete=models.CASCADE, related_name="flights"
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
    Route_CHOICES = [
        ("GONE_TO", "GONE_TO"),
        ("BEEN_TO", "BEEN_TO"),
    ]
    route = models.CharField(choices=Route_CHOICES, max_length=10,
                             default="GONE_TO",null=True,blank=True)

    car: "Car" = models.ForeignKey(
        "cars.Car", on_delete=models.CASCADE, related_name="flights",
        null=True,blank=True
    )

    driver: "Employee" = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE,
        related_name="flights", null=True,blank=True
    )

    departure_date = models.DateField()
    arrival_date = models.DateField(null=True, blank=True)

    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    #
    # price_usd = models.FloatField(
    #     max_length=150,
    #     null=True,
    #     blank=True,
    # )

    driver_expenses_uzs = models.FloatField(
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )

    # driver_expenses_usd = models.FloatField(
    #     help_text="Расходы, выделяемые водителю на рейс",
    #     null=True,
    #     blank=True,
    # )

    cargo_info = models.TextField(blank=True, null=True)


    other_expences = models.FloatField(blank=True, null=True)

    upload = models.ForeignKey(
        "upload.File",
        on_delete=models.SET_NULL,
        related_name="flights",
        null=True,
        blank=True,
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )



    def __str__(self):
        return f"Flight - {self.route} ({self.departure_date})"


class Ordered(TimeStampModel):
    driver_name = models.CharField(max_length=100,null=True,blank=True)
    driver_number = models.CharField(max_length=100,null=True,blank=True)
    car_number = models.CharField(max_length=100,null=True,blank=True)
    cargo_info = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active",
    )
    departure_date = models.DateField()

    price_uzs = models.FloatField(
        max_length=150,
        null=True,
        blank=True,
    )
    driver_expenses_uzs = models.FloatField(
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )
    region: "Region" = models.ForeignKey(
        "region.Region", on_delete=models.CASCADE, related_name="ordered"
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

    def __str__(self):
        return f"Ordered Flight - {self.status} and {self.departure_date}"
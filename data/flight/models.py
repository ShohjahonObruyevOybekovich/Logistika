from django.db import models

from data.cars.models import Car
from data.city.models import Region, City
from employee.models import Employee


class Route(models.Model):
    start : City = models.ForeignKey("City", on_delete=models.CASCADE)
    end : City = models.ForeignKey("City", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start} → {self.end}"


class Flight(models.Model):
    region : Region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name='flights')
    city : City = models.ForeignKey("City", on_delete=models.CASCADE, related_name='flights')
    route:Route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name='flights')
    car : Car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name='flights')
    driver : Employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='flights')

    departure_date = models.DateField()
    arrival_date = models.DateField()

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
    driver_expenses_uzs = models.FloatField(max_length=30,
                                          help_text="Расходы, выделяемые водителю на рейс",
                                              null=True,blank=True)
    driver_expenses_usd = models.FloatField(max_length=30,
                                          help_text="Расходы, выделяемые водителю на рейс",
                                              null=True,blank=True)

    cargo_info = models.TextField(blank=True, null=True)
    uploaded_file = models.FileField(upload_to='flight_files/', blank=True, null=True)
    STATUS_CHOICES = (
        ("ACTIVE" , "Active"),
        ("INACTIVE" , "Inactive")
    )
    status = models.BooleanField(max_length=10,
                                 choices=STATUS_CHOICES,
                                 default="Active")

    def __str__(self):
        return f"Flight  - {self.route} ({self.departure_date})"

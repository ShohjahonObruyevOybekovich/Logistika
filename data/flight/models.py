from django.db import models

from data.cars.models import Car
from data.city.models import Region, City
from employee.models import Employee


class Route(models.Model):
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.start_location} → {self.end_location}"


class Flight(models.Model):
    region : Region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name='flights')
    city : City = models.ForeignKey("City", on_delete=models.CASCADE, related_name='flights')
    route:Route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name='flights')
    car : Car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name='flights')
    driver : Employee = models.ForeignKey("Employee", on_delete=models.CASCADE, related_name='flights')

    departure_date = models.DateField()
    arrival_date = models.DateField()

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                help_text="Введите стоимость рейса")

    driver_expenses = models.DecimalField(max_digits=10,
                                          decimal_places=2,
                                          help_text="Расходы, выделяемые водителю на рейс")

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

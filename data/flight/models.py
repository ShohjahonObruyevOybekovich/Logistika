from django.db import models


class Route(models.Model):
    start = models.ForeignKey(
        "city.City",
        on_delete=models.CASCADE,
        related_name="routes_starting"
    )
    end = models.ForeignKey(
        "city.City",
        on_delete=models.CASCADE,
        related_name="routes_ending"
    )

    def __str__(self):
        return f"{self.start} → {self.end}"


class Flight(models.Model):
    region = models.ForeignKey("city.Region", on_delete=models.CASCADE, related_name="flights")
    city = models.ForeignKey("city.City", on_delete=models.CASCADE, related_name="flights")
    route = models.ForeignKey("flight.Route", on_delete=models.CASCADE, related_name="flights")
    car = models.ForeignKey("cars.Car", on_delete=models.CASCADE, related_name="flights")
    driver = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, related_name="flights")

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

    driver_expenses_uzs = models.FloatField(
        max_length=30,
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )
    driver_expenses_usd = models.FloatField(
        max_length=30,
        help_text="Расходы, выделяемые водителю на рейс",
        null=True,
        blank=True,
    )

    cargo_info = models.TextField(blank=True, null=True)
    upload = models.ForeignKey("upload.File", on_delete=models.CASCADE, related_name="flights")

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

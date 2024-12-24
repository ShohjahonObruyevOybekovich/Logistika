from data.command.models import TimeStampModel
from django.db import models

class Logs(TimeStampModel):

    action = models.CharField(
        choices=[
            ("INCOME", "INCOME"),
            ("OUTCOME", "OUTCOME"),
        ]
        ,max_length=20,
    )
    amount_uzs = models.FloatField()
    amount_usd = models.FloatField()

    car = models.ForeignKey("cars.Car", on_delete=models.SET_NULL, null=True, blank=True)

    employee = models.ForeignKey(
        "employee.Employee", on_delete=models.SET_NULL, null=True, blank=True
    )

    flight = models.ForeignKey(
        "flight.Flight", on_delete=models.SET_NULL, null=True, blank=True
    )

    kind = models.CharField(
        choices=[
            ("OTHER", "Boshqa"),
            ("FIX_CAR", "Avtomobil tuzatish"),
            ("PAY_SALARY", "Oylik berish"),
            ("FLIGHT", "FLIGHT"),
        ], max_length=20
    )

    comment = models.TextField()

    @classmethod
    def create_income(self, amount: float, comment: str):

        Logs.objects.create(
            action="INCOME", amount=amount, kind="OTHER", comment=comment
        )

    @classmethod
    def create_outcome(self, amount: float, comment: str):

        Logs.objects.create(
            action="OUTCOME", amount=amount, kind="OTHER", comment=comment
        )
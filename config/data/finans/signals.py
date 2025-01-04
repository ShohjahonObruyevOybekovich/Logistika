from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Employee
from .models import Logs
from ..flight.models import Flight


@receiver(post_save, sender=Logs)
def on_employee_balance(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "PAY_SALARY" and instance.employee is not None:
        employee = Employee.objects.get(id=instance.employee.id)

        employee_balance = employee.balance_uzs or 0
        salary_amount = instance.amount_uzs or 0

        employee.balance_uzs = employee_balance - salary_amount
        employee.save()


@receiver(post_save, sender=Logs)
def on_salary_balance(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "BONUS" and instance.employee is not None:
        employee = Employee.objects.get(id=instance.employee.id)
        # Ensure `bonus` is not None
        employee.bonus = (employee.bonus or 0) + (instance.amount_uzs or 0)
        employee.save()


@receiver(post_save, sender=Logs)
def on_Salarka(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "SALARKA":
        if instance.flight:
            flight = Flight.objects.filter(id=instance.flight.id).first()
            if flight:
                flight_balance = flight.flight_balance_uzs or 0
                expense_amount = instance.amount_uzs or 0

                flight.flight_balance_uzs = flight_balance - expense_amount
                flight.save()
        else:
            # Log or handle the case where instance.flight is None
            print("Error: instance.flight is None.")


@receiver(post_save, sender=Logs)
def on_flight_expenses(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "FLIGHT" and instance.flight is not None:
        flight = Flight.objects.filter(id=instance.flight.id).first()
        if flight:
            flight_balance = flight.flight_balance_uzs or 0
            expense_amount = instance.amount_uzs or 0

            flight.flight_balance_uzs = flight_balance - expense_amount
            flight.save()

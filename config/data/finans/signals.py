from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Employee
from .models import Logs


@receiver(post_save, sender=Logs)
def on_employee_balance(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "PAY_SALARY" and instance.employee is not None:
        employee = Employee.objects.get(id=instance.employee.id)

        # Ensure balance_uzs and amount_uzs are valid numbers
        employee_balance = employee.balance_uzs if employee.balance_uzs is not None else 0
        salary_amount = instance.amount_uzs if instance.amount_uzs is not None else 0

        # Perform the update
        employee.balance_uzs = employee_balance + salary_amount
        employee.save()

@receiver(post_save, sender=Logs)
def on_salary_balance(sender, instance: Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind == "BONUS" and instance.employee is not None:
        employee = Employee.objects.get(id=instance.employee.id)
        # Ensure `bonus` is not None
        employee.bonus = (employee.bonus or 0) + instance.amount_uzs
        employee.save()
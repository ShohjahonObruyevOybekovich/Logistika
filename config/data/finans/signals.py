from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Employee
from .models import Logs


@receiver(post_save, sender=Logs)
def on_employee_balance(sender, instance:Logs, created, **kwargs):
    if created and instance.action == "OUTCOME" and instance.kind=="PAY_SALARY" and instance.employee is not None:
        driver = Employee.objects.get(id=instance.employee.id)
        driver.balance += instance.amount
        driver.save()

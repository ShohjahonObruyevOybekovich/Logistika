from django.db import models

class Oil(models.Model):
    oil_name = models.CharField(max_length=100, help_text="Oil name")
    oil_volume = models.CharField(max_length=100, help_text="Oil volume litr")
    paid_amount = models.CharField(max_length=100, help_text="Oil paid amount")
    oil_price = models.CharField(max_length=100, help_text="Oil price")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.oil_name


class Remaining_oil_quantity(models.Model):
    oil_volume = models.CharField(max_length=100, help_text="Oil volume litr")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.oil_volume



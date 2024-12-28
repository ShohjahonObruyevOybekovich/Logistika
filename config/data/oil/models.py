from django.db import models

from data.command.models import TimeStampModel


class Oil(TimeStampModel):
    oil_name = models.CharField(max_length=100, help_text="Oil name")
    oil_volume = models.FloatField(help_text="Oil volume in liters")

    purchases: "models.QuerySet[OilPurchase]"

    def __str__(self):
        return self.oil_name


class OilPurchase(TimeStampModel):
    oil = models.ForeignKey("Oil", on_delete=models.CASCADE, related_name="purchases")
    price_uzs = models.FloatField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)


    amount_uzs = models.FloatField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    amount_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)

    oil_volume = models.FloatField(help_text="Oil volume in liters")

    def __str__(self):
        return f"{self.oil.oil_name} - {self.oil_volume} L"

    # class Meta:
    #     ordering = ['-created_at']


class OilREcycles(TimeStampModel):
    oil = models.ForeignKey("Oil", on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Oil price")
    amount_usd = models.FloatField(null=True,blank=True)
    amount_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True
    )
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    remaining_oil = models.FloatField(help_text="Oil remaining")

    def __str__(self):
        return f"{self.oil.oil_name} - {self.remaining_oil} L remaining"


class Remaining_oil_quantity(TimeStampModel):
    oil_volume = models.FloatField(help_text="Oil volume in liters", default=0)

    def __str__(self):
        return f"{self.oil_volume} L"

    @classmethod
    def get(cls):
        return cls.objects.first() or cls.objects.create()


class Utilized_oil(TimeStampModel):
    quantity_utilized = models.FloatField(default=0)
    price_uzs = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_type = models.CharField(choices=[
        ('USD', 'USD'),
        ('UZS', 'UZS'),
        ('KZT', "KZT")
    ],default='USD', max_length=10, null=True, blank=True)

    # price_usd = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Utilized {self.quantity_utilized} L"

    @classmethod
    def get(cls):
        """Retrieve the first instance or create a new one."""
        return cls.objects.first() or cls.objects.create()

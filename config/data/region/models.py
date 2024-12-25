from django.db import models

from data.command.models import TimeStampModel


class Region(TimeStampModel):
    name = models.CharField(max_length=100, help_text="Name of the region")

    price1 = models.FloatField(null=True, blank=True)
    price2 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

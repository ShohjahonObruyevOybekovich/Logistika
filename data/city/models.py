from django.db import models
from data.command.models import TimeStampModel


class Region(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of the region')

    def __str__(self):
        return self.name


class City(TimeStampModel):
    name = models.CharField(max_length=100, help_text='Name of the city')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name}, {self.region.name}"
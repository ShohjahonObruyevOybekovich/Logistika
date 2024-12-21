from django.db import models
from django.http import HttpRequest

from data.command.models import TimeStampModel


class File(TimeStampModel):
    file = models.FileField(upload_to="files")

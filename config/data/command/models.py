from typing import Any
from uuid import uuid4
from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.contrib import admin


class TimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True





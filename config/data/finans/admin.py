from django.contrib import admin

from .models import Logs

# Register your models here.


@admin.register(Logs)
class SaleStudentAdmin(admin.ModelAdmin):
    list_display = ("employee__full_name","action","amount","car__name", "flight__region__name", "created_at")
    search_fields = ("employee__full_name","car__name","flight__region__name")
    list_filter = ("action","kind","amount_type")
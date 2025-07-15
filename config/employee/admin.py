from django.contrib import admin

from employee.models import Employee

admin.site.unregister(Employee)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone","balance","balance_price_type",)
    list_filter = ("balance",)
    search_fields = ("full_name",)
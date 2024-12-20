from django.contrib import admin

from employee.models import Employee

#
# # Register your models here.
# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('user__phone',"user__full_name", "city" ,)
#     search_fields = ('user_phone', 'phone','flight_price')

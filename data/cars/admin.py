from django.contrib import admin

from data.cars.models import Car


#
# # @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ('name', 'number','model_car','car_price')
#     search_fields = ('name','number','model_car','car_price')
#     list_filter = ('name','number','model_car','car_price')
#
#
# # @admin.register(Trailer_cars)
# class Trailer_carsAdmin(admin.ModelAdmin):
#     list_display = ('name','number','model_car','trailer_number')
#     search_fields = ('name','number','model_car','trailer_number')
#     list_filter = ('name','number','model_car','trailer_number')
#
#

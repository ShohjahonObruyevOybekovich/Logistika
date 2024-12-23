from django.contrib import admin
from data.gas.models import *

# @admin.register(GasInventory)
# class GasInventoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'gas_inventory_type', 'gas_inventory_value')
#     list_filter = ('gas_inventory_type',)
#     search_fields = ('gas_inventory_type','gas_inventory_value',)
#
#
# @admin.register(GasPurchase)
# class GasPurchaseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'station_name', 'gas_price','paid_amount','purchased_volume')
#     list_filter = ('purchased_volume','station_name')
#     search_fields = ('station_name',)
#

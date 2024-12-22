from rest_framework import serializers

from data.gas.models import GasStaion


class GasStationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStaion
        fields = ["id", "name", "remaining_gas"]

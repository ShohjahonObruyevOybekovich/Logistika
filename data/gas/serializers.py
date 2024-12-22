from rest_framework import serializers

from data.gas.models import GasStation


class GasStationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStation
        fields = ["id", "name", "remaining_gas"]

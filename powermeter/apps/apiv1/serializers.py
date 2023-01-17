from rest_framework import serializers

from core.models import Device, Metering


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'key', 'name']


class MeteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metering
        fields = ['id', 'device', 'consumption', 'timestamp']

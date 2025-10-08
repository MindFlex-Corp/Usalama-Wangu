from rest_framework import serializers
from Alerts.models import Alert, SMS
from Zones.models import Zone


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'
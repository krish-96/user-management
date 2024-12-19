from rest_framework import serializers
from .models import EventLog, UserLoginEvents


class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = "__all__"

class UserLoginEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginEvents
        fields = "__all__"

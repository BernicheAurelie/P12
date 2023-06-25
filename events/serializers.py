from rest_framework import serializers
from .models import Event, Event_status

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class EventStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event_status
        fields = '__all__'
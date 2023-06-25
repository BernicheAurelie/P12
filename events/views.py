from django.shortcuts import render
from rest_framework import viewsets

from events.models import Event, Event_status
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']
    search_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']

    # def create(self, request, *args, **kwargs):
    #     request.POST._mutable = True
    #     request.data["support_contact"] = request.user.pk
    # 
    #     request.POST._mutable = False
    #     contract__signed_status = True
    #     return super(EventViewSet, self).create(request, *args, **kwargs)

class EventStatusViewSet(viewsets.ModelViewSet):

    queryset = Event_status.objects.all()
    serializer_class = EventStatusSerializer
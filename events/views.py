from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdmin, IsManager, Readonly, IsTechnician, IsSalerForEvents
from utils import logger
from contracts.models import Contract
from events.models import Event, Event_status
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | Readonly | IsSalerForEvents | IsTechnician]
    filterset_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']
    search_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']
    
    def create(self, request, *args, **kwargs):
        logger.debug("Creating event")
        events=Event.objects.filter(contract=self.request.data["contract"])
        logger.debug("Contract already used for another event")
        if events.count()>0:
            return Response(
                {
                    "result": request.data,
                    "message": "An event is already associated to this contract, create a new contract first"
                }
            )
        else:
            contract = Contract.objects.get(id=self.request.data["contract"])
            if contract.signed_status == True :
                if int(self.request.data["client_id"]) == int(contract.client.pk):
                    logger.debug(f"request.data[client_id]: {request.data['client_id']} == contract.client.pk : {contract.client.pk}")
                    super(EventViewSet, self).create(request, *args, **kwargs)
                    return Response(
                        {
                            "result": request.data,
                            "message": "Event successfully created"
                        }
                    )
                else:
                    logger.debug(f"request.data[client_id]: {request.data['client_id']} vs contract.client.pk : {contract.client.pk}")
                    logger.warning("Event not created because contract is for another client")
                    return Response(
                        {
                            "result": request.data,
                            "message": "Impossible to create this event, associated contract and client differents",
                        }
                    )
            else:
                logger.warning("Event not created because contract not signed")
                return Response(
                    {
                        "result": f'contract number: {request.data["contract"]}',
                        "message":"Impossible to create this event, associated contract not signed",
                    }
                )
    
    def update(self, request, *args, **kwargs):
        super(EventViewSet, self).update(request, *args, **kwargs)
        return Response(
                {
                    "result": request.data,
                    "message": "Event successfully updated"
                }
            )

    def get_queryset(self):
        events = Event.objects.all()
        # events = Event.objects.filter(Q (support_contact=self.request.user)| Q (contract__saler_contact=self.request.user))
        return events

class EventStatusViewSet(viewsets.ModelViewSet):

    queryset = Event_status.objects.all()
    serializer_class = EventStatusSerializer

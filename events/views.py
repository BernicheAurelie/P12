from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdmin, Readonly, IsTechnician, IsSalerForEvents
from utils import logger
from contracts.models import Contract
from events.models import Event, Event_status
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdmin | Readonly | IsSalerForEvents | IsTechnician]
    filterset_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']
    search_fields = ['client_id', 'client_id__email', 'event_date', 'event_status']
    
    def create(self, request, *args, **kwargs):
        logger.debug("Creating event")
        request.POST._mutable = True
        events=Event.objects.filter(contract=self.request.data["contract"])
        logger.debug("Contract already used for another event")
        print(events)
        request.POST._mutable = False
        if events:
            return Response(
                {
                    "result": request.data,
                    "message": "An event is already associated to this contract, create a new contract first"
                }
            )
        else:
            contract = Contract.objects.get(id=self.request.data["contract"])
            request.POST._mutable = True
            request.data["client_id"]=contract.client.pk
            request.POST._mutable = False
            # if contract.signed_status is True and request.data["client_id"]==contract.client.pk
            if contract.signed_status is True and request.data["client_id"]==contract.client.pk:
                super(EventViewSet, self).create(request, *args, **kwargs)
                return Response(
                    {
                        "result": request.data,
                        "message": "Event successfully created"
                    }
                )
            elif request.data["client_id"]!=contract.client.pk:
                logger.warning("Event not created")
                return Response(
                    {
                        "result": f'client: {request.data["client_id"]}',
                        "message":"Impossible to create this event, associated contract and client differents",
                    }
                )
            else:
                logger.warning("Event not created")
                return Response(
                    {
                        "result": f'contrat numéro: {request.data["contract"]}',
                        "message":"Impossible to create this event, associated contract not signed",
                    }
                )

    # def create(self, request, *args, **kwargs):
    #     logger.debug("Creating event")
    #     try: 
    #         print("******** bloc try  ******")
    #         request.POST._mutable = True
    #         events=Event.objects.filter(contract=self.request.data["contract"])
    #         logger.debug("Contract already used for another event")
    #         print(events)
    #         request.POST._mutable = False
    #         if events:
    #             return Response(
    #                 {
    #                     "result": request.data,
    #                     "message": "Event already associated to this contract, create a new contract first"
    #                 }
    #             )
    #         else:
    #             return Response(
    #                 {
    #                     "result": request.data,
    #                     "message": "on a un soucis!!! "
    #                 }
    #             )
    #     except:
    #         contract = Contract.objects.get(id=self.request.data["contract"])
    #         request.POST._mutable = True
    #         request.data["client_id"]=contract.client.pk
    #         request.POST._mutable = False
    #         # if contract.signed_status is True and request.data["client_id"]==contract.client.pk
    #         if contract.signed_status is True and request.data["client_id"]==contract.client.pk:
    #             super(EventViewSet, self).create(request, *args, **kwargs)
    #             return Response(
    #                 {
    #                     "result": request.data,
    #                     "message": "Event successfully created"
    #                 }
    #             )
    #         elif request.data["client_id"]!=contract.client.pk:
    #             logger.warning("Event not created")
    #             return Response(
    #                 {
    #                     "result": f'client: {request.data["client_id"]}',
    #                     "message":"Impossible to create this event, associated contract and client differents",
    #                 }
    #             )
    #         else:
    #             logger.warning("Event not created")
    #             return Response(
    #                 {
    #                     "result": f'contrat numéro: {request.data["contract"]}',
    #                     "message":"Impossible to create this event, associated contract not signed",
    #                 }
    #             )
    
    def get_queryset(self):
        events = Event.objects.all()
        # events = Event.objects.filter(Q (support_contact=self.request.user)| Q (contract__saler_contact=self.request.user))
        return events

class EventStatusViewSet(viewsets.ModelViewSet):

    queryset = Event_status.objects.all()
    serializer_class = EventStatusSerializer

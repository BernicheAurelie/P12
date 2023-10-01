from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdmin, IsManager, Readonly, IsTechnician, IsSalerForEvents
from utils import logger
from contracts.models import Contract
from events.models import Event, Event_status
from events.serializers import EventSerializer, EventStatusSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", 'patch', "delete"]
    permission_classes = [
        IsAuthenticated,
        IsAdmin | IsManager | Readonly | IsSalerForEvents | IsTechnician,
    ]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["client_id__email", "client_id__id", "event_date", "event_status__id"]

    class EventFilter(filters.FilterSet):
        event_date = filters.DateFilter(
            field_name="event_date",
            label='date in YYYY-MM-DD',
            lookup_expr='contains'
        )
        client_id = filters.NumberFilter(
            field_name="client_id",
            label='client id'
        )
        client_id__email = filters.CharFilter(
            field_name="client_id__email",
            label='client email'
        )
        STATUS_CHOICES = (
            (1, 'upcoming'),
            (2, 'current'),
            (2, 'finished'),
        )
        event_status = filters.ChoiceFilter(
            field_name='event_status',
            label='event status',
            choices=STATUS_CHOICES
        )

    filterset_fields = ["client_id", "client_id__email", "event_date", "event_status"]
    filterset_class = EventFilter

    def create(self, request, *args, **kwargs):
        logger.debug("Creating event")
        events = Event.objects.filter(contract=self.request.data["contract"])
        if events.count() > 0:
            logger.debug("Contract already used for another event")
            return Response(
                {
                    "result": request.data,
                    "message": "An event is already associated to this contract, \
                        create a new contract first",
                }
            )
        else:
            contract = Contract.objects.get(id=self.request.data["contract"])
            logger.debug(f"Contract n°{contract.id}")
            if contract.signed_status is True:
                if int(self.request.data["client_id"]) == int(contract.client.pk):
                    super(EventViewSet, self).create(request, *args, **kwargs)
                    return Response(
                        {
                            "result": request.data,
                            "message": "Event successfully created",
                        }
                    )
                else:
                    logger.warning(
                        "Event not created because contract is for another client"
                    )
                    return Response(
                        {
                            "result": request.data,
                            "message": "Impossible to create this event, \
                                associated contract and client differents",
                        }
                    )
            else:
                logger.warning("Event not created because contract not signed")
                return Response(
                    {
                        "result": f'contract number: {request.data["contract"]}',
                        "message": "Impossible to create this event, \
                            associated contract not signed",
                    }
                )

    def update(self, request, *args, **kwargs):
        super(EventViewSet, self).update(request, *args, **kwargs)
        return Response(
            {"result": request.data, "message": "Event successfully updated"}
        )

    def get_queryset(self):
        events = Event.objects.all()
        # events = Event.objects.filter(
        # Q (support_contact=self.request.user)| Q (contract__saler_contact=self.request.user)
        # )
        return events


class EventStatusViewSet(viewsets.ModelViewSet):
    queryset = Event_status.objects.all()
    serializer_class = EventStatusSerializer

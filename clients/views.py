from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from permissions import IsAdmin, IsManager, Readonly, IsSalerForClient, IsTechnicianForClients
from utils import logger
from clients.models import Client
from clients.serializers import ClientSerializer
from events.models import Event


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | Readonly | IsSalerForClient | IsTechnicianForClients]
    filterset_fields = ['last_name', 'email']
    search_fields = ['last_name', 'email']

    def perform_create(self, serializer):
        logger.debug("perform_create client")
        try:
            sales_contact = serializer.validated_data['sales_contact']
            serializer.save(sales_contact=sales_contact)
        except KeyError:   
            serializer.save(sales_contact=self.request.user)

    def perform_update(self, serializer):
        logger.debug("perform_update client")
        client = Client.objects.get(id=self.kwargs['pk'])
        try:
            sales_contact = serializer.validated_data['sales_contact']
            serializer.save(sales_contact=sales_contact)
        except KeyError:   
            serializer.save(sales_contact=client.sales_contact)
            
            # first_name = serializer.validated_data["first_name"]
            # last_name=serializer.validated_data["last_name"]
            # email=serializer.validated_data["email"]
            # phone=serializer.validated_data["phone"]
            # company_name=serializer.validated_data["company_name"]

    
    def get_queryset(self):
        clients = Client.objects.all()
        # events = Event.objects.filter(support_contact=self.request.user)
        # associated_clients = [event.client_id.id for event in events]
        # clients = Client.objects.filter(Q (sales_contact_id=self.request.user)| Q (id__in=associated_clients))
        return clients

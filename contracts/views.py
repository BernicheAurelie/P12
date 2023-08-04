from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from permissions import IsAdmin, Readonly, IsSalerForContract
from utils import logger
from contracts.models import Contract
from clients.models import Client
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAdmin | Readonly | IsSalerForContract]
    filterset_fields = ['client', 'client__email', 'client__existing', 'saler_contact', 'date_created', 'amount', 'signed_status', 'payment_due']
    search_fields = ['client', 'client__email', 'client__existing', 'saler_contact', 'date_created', 'amount','payment_due']
    ordering_fields = ['date_created', 'client', 'client__email', 'saler_contact', 'payment_due']

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        client = Client.objects.get(id=self.request.data["client"])
        if client.sales_contact == self.request.user or client.sales_contact==None:
            try:
                saler_contact = request.data['saler_contact']
            except KeyError:
                request.data['saler_contact'] = self.request.user.pk
            try:
                signed_status = request.data['signed_status']
                if signed_status:
                    client.existing = True
                    client.save()
                else:
                    request.data['signed_status']=False
            except KeyError:
                client.existing = False
                client.save()
            request.POST._mutable = False
            super(ContractViewSet, self).create(request, *args, **kwargs)
            return Response(
                {
                    "result": request.data,
                    "message": "Contract successfully created"
                }
            )
        else:
            return Response(
                {
                    "message": "Forbidden, you're not in charge of this client."
                }
            )

    def perform_update(self, serializer):
        client = Client.objects.get(id=self.request.data["client"])
        contract = Contract.objects.get(id=self.kwargs['pk'])
        logger.debug(f"action :  {self.action}, kwargs : {self.kwargs['pk']} client.existing before updating ? :  {client.existing}")
        try:
            saler_contact = serializer.validated_data['saler_contact']
        except KeyError:
            saler_contact = contract.saler_contact
        try:
            signed_status = serializer.validated_data['signed_status']
            if signed_status:
                client.existing = True
                client.save()
            else:
                logger.debug(f"No signed status given: client existing stay {client.existing}")
        except KeyError:
            serializer.validated_data['signed_status'] = False
        logger.debug(f"{client.first_name}, client.existing ? {client.existing}")
        serializer.save(saler_contact=saler_contact)

    def get_queryset(self):
        contracts = Contract.objects.all()
        # clients=Client.objects.filter(sales_contact_id=self.request.user)
        # associated_clients = [client.id for client in clients]
        # contracts = Contract.objects.filter(Q(saler_contact_id = self.request.user)| Q(client_id__in=associated_clients))
        return contracts


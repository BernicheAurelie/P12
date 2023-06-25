from rest_framework import viewsets, filters

from contracts.models import Contract
from clients.models import Client
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filterset_fields = ['client', 'client__email', 'client__existing', 'saler_contact', 'date_created', 'amount', 'signed_status', 'payment_due']
    search_fields = ['client', 'client__email', 'client__existing', 'saler_contact', 'date_created', 'amount','payment_due']
    ordering_fields = ['date_created', 'client', 'client__email', 'saler_contact', 'payment_due']

    def perform_create(self, serializer):
        print("**** serializer : ", serializer)
        print('serializer.validated_data["client"] **** ', self.request.data["client"])
        client = Client.objects.get(id=self.request.data["client"])
        print("serializer.validated_data['saler_contact']", serializer.validated_data['saler_contact'])
        if not serializer.validated_data['saler_contact'] :
            print("not particular saler: connected user given by default => ", self.request.user.pk)
            serializer.validated_data['saler_contact']=self.request.user
            # serializer.save(saler_contact=self.request.user)
        elif serializer.validated_data['signed_status']:
            print('signed status')
            client.existing = True
            client.save()
        serializer.save()

    # def create(self, request, *args, **kwargs):
    #     print("request etc ***** ", request, *args, **kwargs)
    #     print("request etc ***** ", request.data)
    #     request.POST._mutable = True
    #     if not request.data["saler_contact"]:
    #         request.data["saler_contact"] = request.user.pk
    #     client = Client.objects.get(id=request.data["client"])
    #     try: 
    #         print("client found? signed_status true")
    #         if request.data["signed_status"] is True:
    #             print("signed_status true")
    #             client.existing = True
    #             print("client update existing")
    #         else:
    #             print("signed_status false")
    #     except:
    #         print("client not found? or signed_status false")
    #     request.POST._mutable = False
    #     return super(ContractViewSet, self).create(request, *args, **kwargs)
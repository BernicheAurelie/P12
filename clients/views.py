from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['last_name', 'email']
    search_fields = ['last_name', 'email']

    def perform_create(self, serializer):
        print("**** serializer : ", serializer)
        if not serializer.validated_data['sales_contact']:
            serializer.save(sales_contact=self.request.user)
        else:    
            serializer.save()
            

    # def create(self, request, *args, **kwargs):
    #     request.POST._mutable = True
    #     request.data["sales_contact"] = request.user.pk
    #     request.POST._mutable = False
    #     return super(ClientViewSet, self).create(request, *args, **kwargs)
    
    def get_queryset(self):
        clients = Client.objects.filter(sales_contact_id = self.request.user)
        return clients

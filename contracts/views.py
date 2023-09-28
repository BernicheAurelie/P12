from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from permissions import IsAdmin, IsManager, Readonly, IsSalerForContract
from utils import logger
from contracts.models import Contract
from clients.models import Client
from contracts.serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdmin | IsManager | Readonly | IsSalerForContract,
    ]
    filterset_fields = [
        "client",
        "client__email",
        "client__existing",
        "saler_contact",
        "date_created",
        "amount",
        "signed_status",
        "payment_due",
    ]
    search_fields = [
        "client",
        "client__email",
        "client__existing",
        "saler_contact",
        "date_created",
        "amount",
        "payment_due",
    ]
    ordering_fields = [
        "date_created",
        "client",
        "client__email",
        "saler_contact",
        "payment_due",
    ]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        client = Client.objects.get(id=self.request.data["client"])
        if client.sales_contact == self.request.user or client.sales_contact == None:
            try:
                saler_contact = request.data["saler_contact"]
            except KeyError:
                request.data["saler_contact"] = self.request.user.pk
            request.POST._mutable = False
            super(ContractViewSet, self).create(request, *args, **kwargs)
            try:
                signed_status = request.data["signed_status"]
                if signed_status == "true":
                    client.existing = True
                    client.save()
                else:
                    logger.warning(
                        f"Signed status false: client maybe existing with another contract"
                    )
            except KeyError:
                logger.info(
                    f"Signed status not given: client existing stay {client.existing}"
                )
            return Response(
                {"result": request.data, "message": "Contract successfully created"}
            )
        elif self.request.user.is_admin == True or self.request.user.role.pk == 2:
            try:
                saler_contact = request.data["saler_contact"]
                super(ContractViewSet, self).create(request, *args, **kwargs)
                try:
                    signed_status = request.data["signed_status"]
                    if signed_status == "true":
                        client.existing = True
                        client.save()
                    else:
                        logger.warning(
                            f"Signed status false: client existing stay {client.existing}"
                        )
                except KeyError:
                    logger.info(
                        f"Signed status not given: client existing stay {client.existing}"
                    )
                return Response(
                    {"result": request.data, "message": "Contract successfully created"}
                )
            except KeyError:
                return Response(
                    {
                        "message": "saler_contact is required to create contract for managers or administrators"
                    }
                )
        else:
            logger.info("you're not client sales_contact")
            return Response(
                {"message": "Forbidden, you're not in charge of this client."}
            )

    def update(self, request, *args, **kwargs):
        client = Client.objects.get(id=self.request.data["client"])
        contract = Contract.objects.get(id=self.kwargs["pk"])
        if (
            contract.saler_contact == self.request.user
            or contract.saler_contact == None
        ):
            try:
                saler_contact = request.data["saler_contact"]
            except KeyError:
                request.POST._mutable = True
                request.data["saler_contact"] = contract.saler_contact.pk
                request.POST._mutable = False
            try:
                signed_status = request.data["signed_status"]
                if signed_status == "true":
                    super(ContractViewSet, self).update(request, *args, **kwargs)
                    client.existing = True
                    client.save()
                else:
                    logger.warning(
                        f"Signed status not True: client existing stay {client.existing}"
                    )
                    super(ContractViewSet, self).update(request, *args, **kwargs)
            except KeyError:
                super(ContractViewSet, self).update(request, *args, **kwargs)
            return Response(
                {"result": request.data, "message": "Contract successfully updated"}
            )
        elif self.request.user.is_admin == True or self.request.user.role.pk == 2:
            super(ContractViewSet, self).update(request, *args, **kwargs)
            try:
                signed_status = request.data["signed_status"]
                if signed_status == "true":
                    client.existing = True
                    client.save()
                else:
                    logger.warning(
                        f"Signed status false: client existing stay {client.existing}"
                    )
            except KeyError:
                logger.info(
                    f"Signed status not given: client existing stay {client.existing}"
                )
            return Response(
                {"result": request.data, "message": "Contract successfully updated"}
            )
        else:
            logger.info("you're not the client sales_contact")
            return Response(
                {
                    "message": "Forbidden, you're neither in charge of this client nor manager or administrator."
                }
            )

    def get_queryset(self):
        contracts = Contract.objects.all()
        # clients=Client.objects.filter(sales_contact_id=self.request.user)
        # associated_clients = [client.id for client in clients]
        # contracts = Contract.objects.filter(Q(saler_contact_id = self.request.user)| Q(client_id__in=associated_clients))
        return contracts

from rest_framework.permissions import BasePermission
from contracts.models import Contract
from clients.models import Client
from events.models import Event
from utils import logger


class IsAdmin(BasePermission):
    logger.debug("Are you administrator?")

    def has_permission(self, request, view):
        logger.debug(f"class IsAdmin: action = {view.action}")
        if request.user.is_admin:
            logger.info(f"allowed {request.user}, you're administrator")
            return True
        else:
            logger.warning("Only allowed to administration")
            return False


class Readonly(BasePermission):
    def has_permission(self, request, view):
        logger.debug(f"class Read Only: action = {view.action}")
        if view.action in ("list", "retrieve"):
            logger.info(
                f"allowed {request.user}, you can read clients, contracts and events"
            )
            return True
        else:
            logger.warning("Only allowed to read informations")
            return False


class IsManager(BasePermission):
    logger.debug("Are you manager to access full ORM?")

    def has_permission(self, request, view):
        logger.debug(f"class IsManager: action = {view.action}")
        if request.user.role.pk == 2:
            logger.info(f"{request.user}: allowed, you can {view.action} an user")
            return True
        else:
            logger.warning("Only allowed to manager team")
            return False


# class IsOwnerProfile(BasePermission):
#     logger.debug("Is you're own profile?")

#     def has_permission(self, request, view):
#         logger.debug("user profile?")
#         try:
#             user = User.objects.get(id=view.kwargs["pk"])
#             if user.id == request.user.pk and view.action in (
#                 "list",
#                 "retrieve",
#                 "update",
#                 "partial_update",
#             ):
#                 logger.info(
#                     f"{request.user}: allowed, \
#                         you can get and update your profile but not delete it"
#                 )
#                 return True
#         except KeyError:
#             logger.warning(
#                 f"{request.user}: you are {request.user.role}. Manage users forbidden"
#             )
#             return False


class IsSalerForClient(BasePermission):
    logger.debug("Are you saler to access clients?")

    def has_permission(self, request, view):
        logger.debug(
            f"is saler? {request.user}, you're {request.user.role}, trying to: {view.action}"
        )
        try:
            client = Client.objects.get(id=view.kwargs["pk"])
            logger.debug(f"{request.user}, client number: {view.kwargs['pk']}")
            if client.sales_contact == request.user:
                logger.info(
                    f"{request.user}, ok, you're sales contact :{client.sales_contact}"
                )
                return True
            else:
                logger.warning(
                    f"{request.user.role} => not sales contact, update or delete forbidden"
                )
                return False
        except KeyError:
            logger.debug(f"{request.user}, client doesn't found => create or list")
            if request.user.role.pk == 1:
                logger.info("Saler: allowed to create clients")
                return True
            else:
                logger.warning(
                    f"{request.user.role} => not saler => forbidden to create clients"
                )
                return False


class IsSalerForContract(BasePermission):
    logger.debug("Are you saler to access contracts?")

    def has_permission(self, request, view):
        logger.debug(
            f"is saler? {request.user}, you're {request.user.role}, trying to: {view.action}"
        )
        try:
            contract = Contract.objects.get(id=view.kwargs["pk"])
            client = contract.client
            logger.debug(
                f"associated client? {client}, sales_contact.id: {client.sales_contact.id}"
            )
            if contract.saler_contact.id == request.user.pk:
                logger.info(
                    f"{request.user}, ok, you're saler contact for the contract"
                )
                return True
            else:
                logger.warning(
                    f"{request.user} => you're not in charge => {view.action} is forbidden"
                )
                return False
        except KeyError:
            logger.debug(f"{request.user}, contract doesn't found => create or list")
            if request.user.role.pk == 1:
                logger.info("Saler: allowed to create and get contracts")
                return True
            else:
                logger.warning(
                    f"{request.user.role} => not saler => forbidden to create contracts"
                )
                return False


class IsSalerForEvents(BasePermission):
    # allowed to create event when in charge for the contract
    logger.debug("Are you saler contact to create events?")

    def has_permission(self, request, view):
        logger.debug(
            f"is saler contact for the contract? {request.user}, \
                you're {request.user.role}, trying to: {view.action}"
        )
        try:
            logger.debug("try to create event for the saler")
            contract = Contract.objects.get(id=request.data["contract"])
            logger.debug(
                f"try to create event for the saler for contract: {contract.id}"
            )
            if contract.saler_contact.id == request.user.pk:
                if view.action == "create":
                    return True
                else:
                    logger.warning(
                        f"saler contact can't {view.action}, \
                            only allowed to technician, manager or administrator"
                    )
                    return False
            else:
                logger.warning(
                    f"Forbidden: saler contact for the contract is {contract.saler_contact}"
                )
                return False
        except KeyError:
            logger.warning("Contract not found")
            return False


class IsTechnician(BasePermission):
    # allowed to CRUD for an event when is support_contact
    # and CRUD for associated client (event.client_id)
    logger.debug("Are you technician to access events?")

    def has_permission(self, request, view):
        logger.debug(
            f"is technician? {request.user}, you're {request.user.role}, trying to: {view.action}"
        )
        try:
            event = Event.objects.get(id=view.kwargs["pk"])
            logger.debug(f"event n°{view.kwargs['pk']}")
            if event.support_contact.id == request.user.pk:
                logger.info(
                    f"Allowed {request.user}: you are support for event n°{view.kwargs['pk']}"
                )
                return True
            else:
                logger.warning(f"{request.user} => {view.action} is forbidden")
                return False
        except KeyError:
            logger.debug(
                f"{request.user}, event doesn't found, \
                    create event allowed to saler contact, manager or administrator"
            )
            logger.warning(f"{request.user} => {view.action} is forbidden")
            return False

from rest_framework.routers import SimpleRouter
from .views import ContractViewSet


app_name = "contracts"

router = SimpleRouter(trailing_slash=False)
router.register(r"contracts/?", ContractViewSet, basename="contracts")

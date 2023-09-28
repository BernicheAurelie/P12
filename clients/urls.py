from rest_framework.routers import SimpleRouter
from .views import ClientViewSet


app_name = "clients"

router = SimpleRouter(trailing_slash=False)
router.register(r"clients/?", ClientViewSet, basename="clients")

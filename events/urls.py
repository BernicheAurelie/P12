from rest_framework.routers import SimpleRouter
from .views import EventViewSet


app_name = "events"

router = SimpleRouter(trailing_slash=False)
router.register(r"events/?", EventViewSet, basename='events')

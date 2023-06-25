from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserViewSet


app_name = "users"

router = SimpleRouter(trailing_slash=False)
router.register(r"users/?", UserViewSet, basename='users')

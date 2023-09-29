from rest_framework.routers import SimpleRouter
from .views import UserViewSet
# from .views import UserList, UserDetail


app_name = "users"

router = SimpleRouter(trailing_slash=False)
router.register(r"users/?", UserViewSet, basename="users")
# router.register(r"users", UserList, basename="users")
# router.register(r"users/?", UserDetail, basename="users")

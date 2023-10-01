from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from permissions import IsManager, IsAdmin
from users.models import User, User_role
from users.serializers import UserSerializer, UserListSerializer, UserRoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    permission_classes = [IsAuthenticated, IsAdmin | IsManager]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role__id", "is_admin"]
    search_fields = ["username", "email"]
    ordering_fields = ["role", "username"]

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        else:
            return UserSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = User_role.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

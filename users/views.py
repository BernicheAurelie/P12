from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from permissions import IsManager, IsAdmin, IsOwnerProfile
from users.models import User, User_role
from users.serializers import UserSerializer, UserListSerializer, UserRoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | IsOwnerProfile]
    filterset_fields = ["role", "is_admin"]
    search_fields = ["username", "email"]
    ordering_fields = ["role", "username"]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = User_role.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

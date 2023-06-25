from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import User, User_role
from users.serializers import UserSerializer, UserRoleSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    filterset_fields = ['role','is_admin']
    search_fields = ['username','email']
    ordering_fields = ['role', 'username']


class UserRoleViewSet(viewsets.ModelViewSet):

    queryset = User_role.objects.all()
    serializer_class = UserRoleSerializer
    # permission_classes = [IsAuthenticated]


# from rest_framework import generics
# 
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
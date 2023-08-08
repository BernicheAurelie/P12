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
    filterset_fields = ['role','is_admin']
    search_fields = ['username','email']
    ordering_fields = ['role', 'username']

    # def create(self, request, *args, **kwargs):
    #     password=request.data["password"]
    #     super(UserViewSet, self).create(request, *args, **kwargs)
    #     user=User.objects.get(username=request.data['username'])
    #     user.set_password(password)
    #     user.save()
    #     return Response(
    #         {
    #             "result": request.data,
    #             "message": "User successfully created"
    #         }
    #     )
    
    def perform_create(self, serializer):
        password = serializer.validated_data['password']
        username = serializer.validated_data['username']
        serializer.save()
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

    def perform_update(self, serializer):
        user = User.objects.get(id=self.kwargs['pk'])
        # print("serializer.data: ", serializer.validated_data)
        try: 
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            serializer.save()
        except KeyError:
            password = user.password
            user.set_password(password)
            user.save()
            serializer.save()
        # print("user password **************", user.password)
          

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


# from rest_framework import generics
# 
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
from rest_framework import serializers
from .models import User, User_role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "role",
            "is_admin",
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "is_admin",
        ]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_role
        fields = "__all__"

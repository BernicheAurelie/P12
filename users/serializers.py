from rest_framework import serializers
from .models import User, User_role
from utils import logger


class UserSerializer(serializers.ModelSerializer):
    # role = serializers.StringRelatedField()
    # role = serializers.CharField(source='user_role')
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "role",
            "is_admin",
        ]

    def create(self, validated_data):
        logger.debug("********** CREATE METHOD IN SERIALIZER ***********")
        user = User.objects.create(**validated_data)
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        logger.debug("********** UPDATE METHOD IN SERIALIZER ***********")
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


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

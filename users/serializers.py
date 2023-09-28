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
        logger.debug("HERE IS THE CREATE METHOD IN SERIALIZER µµµ")
        user = User.objects.create(**validated_data)
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        logger.debug("HERE IS THE UPDATE METHOD IN SERIALIZER ********* ")
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     logger.debug("HERE IS THE UPDATE METHOD IN SERIALIZER ********* ")
    #     user = User.objects.get(id=instance.id)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.role = validated_data.get('role', instance.role)
    #     instance.is_admin = validated_data.get('is_admin', instance.is_admin)
    #     instance.save()
    #     user.set_password(instance.password)
    #     user.save()
    #     # if validated_data["password"]:
    #     #     # instance.save()
    #     #     logger.debug("HERE IS THE UPDATE METHOD with change PASSWORD")
    #     #     password = validated_data["password"]
    #     #     print("password", password)
    #     #     user.set_password(password)
    #     #     user.save()
    #     #     print("user.password", user.password)
    #     #     # instance.save()

        # else:
        #     logger.debug("user password not changed in serializer")
        #     # instance.save()
# si je sauvegarde après le set_password => ça marche pas
# Mais pour les tests, ça ne fonctionne que si instance.save() est après !!!
        # instance.save()
        return instance
    
    # def create(self, validated_data):
    #     print("CREATE METHODE IN SERIALIZER ********")
    #     password = validated_data["password"]
    #     user = User.objects.create(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    
    # def update(self, validated_data):
    #     print("update METHODE IN SERIALIZER ********")
    #     user = User.objects.get(id=self.kwargs["pk"])
    #     try:
    #         password = validated_data["password"]
    #         user.set_password(password)
    #         user.save()
    #     except:
    #         password = user.password
    #         user.save()
    #         # user_updated = User.objects.update(**validated_data)
    #         # user_updated.save()
    #     return super().update(validated_data)

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

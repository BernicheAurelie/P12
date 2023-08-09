from django.db import models
from django.contrib.auth.models import AbstractUser


class User_role(models.Model):
    SALER = "saler"
    MANAGER = "manager"
    TECHNICIAN = "technician"
    CHOICES = [(SALER, ("saler")), (MANAGER, ("manager")), (TECHNICIAN, ("technician"))]
    user_role = models.CharField(max_length=10, choices=CHOICES, default="saler")

    def __str__(self):
        return f"{self.user_role}"

    class Meta:
        verbose_name = "user_role"
        verbose_name_plural = "users_roles"


class User(AbstractUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.ForeignKey(
        User_role,
        on_delete=models.SET_DEFAULT,
        default="saler",
        null=True,
        related_name="role",
    )
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

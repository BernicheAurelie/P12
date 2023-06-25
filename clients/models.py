from django.db import models
from users.models import User


class Client(models.Model):
    
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='saler_id')
    existing = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
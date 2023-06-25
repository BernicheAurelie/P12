from django.db import models
from django.utils import timezone
from users.models import User
from clients.models import Client


class Contract(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client')
    saler_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='saler')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    signed_status = models.BooleanField(default=False) # or True?
    amount = models.FloatField()
    payment_due = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self) -> str:
        return f"Contract n°{self.id}"

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'

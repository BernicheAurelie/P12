from django.db import models
from django.utils import timezone, dateformat
from datetime import date
from django.utils.html import format_html
from users.models import User
from clients.models import Client


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client")
    saler_contact = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="saler"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    signed_status = models.BooleanField(default=False)  # or True?
    amount = models.FloatField()
    payment_due = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self) -> str:
        return f"Contract n°{self.id}"

    def colored_payment_due(self):
        payment_due = dateformat.format(self.payment_due, "N-d-Y")
        if self.payment_due is None or self.payment_due > timezone.now():
            color = "green"
        elif self.payment_due < timezone.now():
            color = "red"
        else:
            color = "orange"
        return format_html("<span style=color:%s>%s</span>" % (color, payment_due))

    colored_payment_due.allow_tags = True

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

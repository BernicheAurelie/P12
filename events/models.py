from django.db import models
from django.utils import timezone
from users.models import User
from clients.models import Client
from contracts.models import Contract


class Event_status(models.Model):
    UPCOMING = 'upcoming'
    CURRENT = 'current'
    FINISHED = 'finished'
    CHOICES = [(UPCOMING, ('upcoming')), (CURRENT, ('current')), (FINISHED, ('finished'))]
    tag = models.CharField(max_length=8, choices=CHOICES, default='upcoming')

    def __str__(self):
        return f"{self.tag}"

    class Meta:
        verbose_name = 'Event_status'
        verbose_name_plural = 'Events_status'


class Event(models.Model):
    
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_id')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='support_id')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_id')
    attendees = models.IntegerField()
    event_status = models.ForeignKey(Event_status, on_delete=models.SET_DEFAULT, default='upcoming', related_name='event_status')
    event_date = models.DateTimeField(auto_now_add=False, default=timezone.now)
    notes = models.TextField(max_length=500)

    def __str__(self):
        return f"Event n°{self.id}"

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
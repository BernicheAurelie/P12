from django.contrib import admin
from .models import Contract

# Register your models here.
# admin.site.register(Contract)

def change_signed_status(modeladmin, request, queryset):
    queryset.update(signed_status='True')
change_signed_status.short_description = 'Change selected contracts status to signed'

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['id','client', 'saler_contact', 'date_created', 'date_updated', 'signed_status', 'amount', 'payment_due', 'colored_payment_due']
    search_fields = ['client', 'saler_contact', 'date_created', 'date_updated', 'signed_status', 'amount', 'payment_due']
    list_filter = ['client', 'saler_contact', 'date_created', 'date_updated', 'signed_status', 'amount', 'payment_due']
    actions = [change_signed_status]
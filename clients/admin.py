from django.contrib import admin
from .models import Client

# Register your models here.
# admin.site.register(Client)


def change_existing_client(modeladmin, request, queryset):
    queryset.update(existing="True")


change_existing_client.short_description = "Change selected clients as existing"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # form = UserForm
    # exclude = ('')
    # what we see in admin:
    list_display = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_created",
        "date_updated",
        "sales_contact",
        "existing",
    ]
    # filters and search fields
    list_filter = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_created",
        "date_updated",
        "sales_contact",
        "existing",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "date_created",
        "date_updated",
        "sales_contact",
        "existing",
    )
    actions = [change_existing_client]

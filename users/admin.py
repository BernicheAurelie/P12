from django.contrib import admin
from .models import User, User_role

# from .forms import UserForm


def change_is_admin(modeladmin, request, queryset):
    queryset.update(is_admin="True")


change_is_admin.short_description = "Change selected users as admin"

admin.site.register(User_role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # form = UserForm
    # exclude = ('')
    # what we see in admin:
    list_display = ("first_name", "last_name", "username", "email", "role", "is_admin")
    # filters and search fields
    list_filter = ("role", "is_admin")
    search_fields = ("first_name", "last_name", "username", "email", "role", "is_admin")
    actions = [change_is_admin]


admin.site.site_header = "EPIC EVENTS"
admin.site.site_title = "EPIC EVENTS ORM"
admin.site.index_title = "Welcome to EPIC EVENTS"

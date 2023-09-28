from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, User_role
from .forms import UserForm


def change_is_admin(modeladmin, request, queryset):
    queryset.update(is_admin="True")


change_is_admin.short_description = "Change selected users as admin"

admin.site.register(User_role)


class MyUserAdmin(UserAdmin):
    add_form = UserForm
    model = User
    # fields in your custom user model:
    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
        "role",
        "password",
        "is_admin",
    )
    # fields in your custom user model intended for filtering:
    list_filter = ("role", "is_admin")
    # fields in your custom user model intended for searching:
    search_fields = ("first_name", "last_name", "username", "email", "role", "is_admin")
    # fields in your custom user model intended for ordering:
    ordering = ("username", "email", "role")
    filter_horizontal = ()  # Leave it empty. You have neither `groups` or `user_permissions`
    add_fieldsets = (
        ("login informations", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("status", {"fields": ("is_admin", "role")}),
    )
    actions = [change_is_admin]


admin.site.register(User, MyUserAdmin)

admin.site.site_header = "EPIC EVENTS"
admin.site.site_title = "EPIC EVENTS ORM"
admin.site.index_title = "Welcome to EPIC EVENTS"

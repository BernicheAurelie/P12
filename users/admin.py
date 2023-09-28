from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, User_role
from .forms import UserForm



def change_is_admin(modeladmin, request, queryset):
    queryset.update(is_admin="True")


change_is_admin.short_description = "Change selected users as admin"

admin.site.register(User_role)


# @admin.register(User)
# class UserAdminCustom(admin.ModelAdmin):
#     # what we see in admin:
#     list_display = ("first_name", "last_name", "username", "email", "role", "is_admin")
#     ordering = ("username", "email", "role")
#     # filters and search fields
#     list_filter = ("role", "is_admin")
#     search_fields = ("first_name", "last_name", "username", "email", "role", "is_admin")
#     actions = [change_is_admin]


class MyUserAdmin(UserAdmin):
    add_form = UserForm
    model = User
    list_display = ("first_name", "last_name","username", "email", "role", "password", "is_admin")  # Contain only fields in your `custom-user-model`
    list_filter = ("role", "is_admin")  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    search_fields = ("first_name", "last_name", "username", "email", "role", "is_admin")  # Contain only fields in your `custom-user-model` intended for searching
    ordering = ("username", "email", "role")  # Contain only fields in your `custom-user-model` intended to ordering
    filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
    # fieldsets = ({'fields': ("first_name", "last_name", "username", "email", "password" ,"role", "is_admin")})
    # fieldsets = (('login informations', {'fields': ('username', 'password')}), 
    #  ('Personal info', {'fields': ('first_name', 'last_name', 'email')}), 
    #  ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
    #  ('Important dates', {'fields': ('last_login', 'date_joined')}), 
    #  ('status', {'fields': ('is_admin', 'role')}))
    add_fieldsets = (('login informations', {'fields': ('username', 'password')}), 
     ('Personal info', {'fields': ('first_name', 'last_name', 'email')}), 
     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
     ('Important dates', {'fields': ('last_login', 'date_joined')}), 
     ('status', {'fields': ('is_admin', 'role')}))
    actions = [change_is_admin]
    

admin.site.register(User, MyUserAdmin)

# admin.site.unregister(User)
# admin.site.register(User, UserAdminCustom)
admin.site.site_header = "EPIC EVENTS"
admin.site.site_title = "EPIC EVENTS ORM"
admin.site.index_title = "Welcome to EPIC EVENTS"

# from django.forms import ModelForm
# from .models import User


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "password", "first_name", "last_name", 'email', "role", "is_admin")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
    
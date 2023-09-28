from django.forms import ModelForm
from .models import User
from utils import logger


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", 'email', "role", "is_admin")

    def save(self, commit=True):
        logger.debug("************* save method in userform")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from .models import CustomUser


# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ("email",)


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ("email",)
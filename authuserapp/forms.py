from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# login form only expects a user id
class LoginUserForm(forms.Form):
    user_id = forms.CharField(label="user_id")

    def clean_user_id(self):
        user_id_clean = self.cleaned_data['user_id'].upper()

        return user_id_clean

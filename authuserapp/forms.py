from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authuserapp.models import InventoryItem


# login form only expects a user id
# class LoginUserForm(forms.Form):
#     user_id = forms.CharField(label="user_id")

#     def clean_user_id(self):
#         user_id_clean = self.cleaned_data['user_id'].upper()

#         return user_id_clean

class LoginUserForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class InventoryForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['sku', 'price', 'count', 'status']
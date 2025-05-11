from django.forms import ModelForm
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from phonenumber_field.formfields import PhoneNumberField

from .models import Info

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Login Uniandes',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class InfoUpdateForm(ModelForm):
    class Meta:
        model = Info

        fields = ['bachelor', 'phone']
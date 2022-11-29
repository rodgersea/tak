from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.fields import EmailField
from django.forms.forms import Form
from django import forms
from .models import *

area_datalist = Route.objects.all().values_list('area', flat=True)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ClimbElementForm(forms.Form):
    area = forms.CharField(max_length=50)
    sector = forms.CharField(max_length=50)
    crag = forms.CharField(max_length=50)
    wall = forms.CharField(max_length=50)
    route = forms.CharField(max_length=50)

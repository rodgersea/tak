from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

area_datalist = Route.objects.all().values_list('area', flat=True)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ClimbElementForm(forms.Form):
    area = forms.CharField(max_length=50)
    sector = forms.CharField(max_length=50)
    crag = forms.CharField(max_length=50)
    wall = forms.CharField(max_length=50)
    route = forms.CharField(max_length=50)


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from .models import *
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
 
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'first_name', 'last_name']


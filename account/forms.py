from cProfile import label
from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text='*Required')
    username = forms.CharField (max_length=10, help_text='*Required')
    class Meta:
        model = Account
        fields = ['email','username','password1', 'password2']
        exclude = []


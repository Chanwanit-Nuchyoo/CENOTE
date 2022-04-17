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

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username','info','profile_image','github','contact_email','youtube']

        widgets = {
            'username': forms.TextInput(attrs={
                'type':'text',
                'placeholder':'Username...',
                'required':'',
            }),
            'info':forms.Textarea(attrs={
                'type':'text',
                'placeholder':'Info...',
            }),

            'contact_email':forms.TextInput(attrs={
                'type':'email',
                'placeholder':'Contact Email...',
            }),

            'github':forms.TextInput(attrs={
                'type':'url',
                'placeholder':'Github...',
            }),
            'youtube':forms.TextInput(attrs={
                'type':'url',
                'placeholder':'Youtube...',
            }),

            'profile_image': forms.FileInput(attrs={
                'name':'profilePic',
                'type':'file',
                'accept':'image/*',
            }),
        }
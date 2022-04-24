from cProfile import label
from dataclasses import field
import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db.models.functions import Length
from account.models import Account

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=10,min_length=4)

    class Meta:
        model = Account
        fields = ['email','username','password1', 'password2']        
        widgets = {
            'email': forms.EmailInput(attrs={
                'type':'email',
                'required': True,
                'style':'border-radius: 10px; width:100%; height: 40px;',
                'oninput':"this.value=this.value.replace(/[^a-zA-Z0-9@._-]/g,'');"
            }),

            'username': forms.TextInput(attrs={
                'type':'text',
                'required': True,
                'style':'border-radius: 10px; width:100%; height: 40px;',
                'oninput':"this.value=this.value.replace(/[^a-zA-Z0-9]/g,'');",
                'minlength': 4,
                'maxlength': 10,
            }),
        }

class AccountEditForm(forms.ModelForm):
    
    username = forms.CharField(max_length=10,min_length=4)

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
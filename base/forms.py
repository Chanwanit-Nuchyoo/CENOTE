from django import forms
from base.models import Note, Comment, Category,Images
from account.models import Account

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','info','price','category']

class NoteEditForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','info','price','category','pdf_file']
'''
class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = []
        exclude = []
'''

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

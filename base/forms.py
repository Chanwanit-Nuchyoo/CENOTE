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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'type':'text',
                'placeholder':'Type something...',
                'cols': 105,
                'rows': 3,
                'required':'',
                'TextMode':'MultiLine',
                'style':'font-size:20px; border-radius:10px; resize: none; background-color: #444444; color: white; padding:5px',
            }),
        }

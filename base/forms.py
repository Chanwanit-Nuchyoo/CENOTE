from django import forms
from base.models import Note, Comment, Category,Images

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','info','price','category','pdf_file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
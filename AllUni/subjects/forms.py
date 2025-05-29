from django import forms
from .models import Subject, Note
from simplemde.fields import SimpleMDEField

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']  

class NoteForm(forms.ModelForm):
    content = SimpleMDEField()
    
    class Meta:
        model = Note
        fields = ['title', 'content']
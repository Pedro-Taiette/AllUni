from django import forms
from .models import Subject, Note

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']  

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content'] 
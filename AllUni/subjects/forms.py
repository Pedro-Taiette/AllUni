from django import forms
from .models import Subject, Note
from simplemde.fields import SimpleMDEField

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'color']
        widgets = {
            'color': forms.Select(choices=[
                ('blue', 'Azul'),
                ('green', 'Verde'),
                ('red', 'Vermelho'),
                ('yellow', 'Amarelo'),
                ('purple', 'Roxo'),
                ('pink', 'Rosa'),
                ('gray', 'Cinza'),
            ])
        }

class NoteForm(forms.ModelForm):
    content = SimpleMDEField()
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'is_favorite']
        widgets = {
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

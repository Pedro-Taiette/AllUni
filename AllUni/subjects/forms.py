from django import forms
from .models import Subject, Note
from simplemde.fields import SimpleMDEField

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'color']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'color': forms.Select(choices=[
                ('blue', 'Azul'),
                ('green', 'Verde'),
                ('red', 'Vermelho'),
                ('yellow', 'Amarelo'),
                ('purple', 'Roxo'),
                ('pink', 'Rosa'),
                ('gray', 'Cinza'),
            ], attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'})
        }

class NoteForm(forms.ModelForm):
    content = SimpleMDEField()
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'is_favorite']
        widgets = {
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
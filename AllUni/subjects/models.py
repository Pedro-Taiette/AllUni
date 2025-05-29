# subjects/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import markdown2

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="blue")
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(default=timezone.now)  
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def get_note_count(self):
        return self.notes.count()
    
    def get_recent_notes(self, limit=5):
        return self.notes.order_by('-created_at')[:limit]
    
    def get_slug(self):
        return slugify(self.name)


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(default=timezone.now)  
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def get_html_content(self):
        """Converte o conteúdo Markdown para HTML."""
        return markdown2.markdown(self.content)
    
    def get_reading_time(self):
        """Calcula o tempo estimado de leitura em minutos."""
        word_count = len(self.content.split())
        minutes = word_count // 200  # Média de 200 palavras por minuto
        return max(1, minutes)  # Pelo menos 1 minuto
    
    def get_excerpt(self, chars=100):
        """Retorna um trecho do conteúdo."""
        if len(self.content) <= chars:
            return self.content
        return self.content[:chars] + "..."
    
    def is_recently_updated(self, days=1):
        """Verifica se a nota foi atualizada recentemente."""
        from django.utils import timezone
        import datetime
        return self.updated_at >= (timezone.now() - datetime.timedelta(days=days))

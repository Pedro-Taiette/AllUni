from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def get_html_content(self):
        """Converte o conteúdo Markdown para HTML."""
        import markdown2
        return markdown2.markdown(self.content)

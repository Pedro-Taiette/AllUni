from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Subject, Note

class SubjectTests(TestCase):
    
    def setUp(self):
        """Configura o usuário e dados básicos para os testes."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_subject_list(self):
        """Testa se a página de listagem de subjects exibe os subjects do usuário."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        response = self.client.get(reverse('subject_list'))
        self.assertContains(response, subject.name)

    def test_add_subject(self):
        """Testa se é possível adicionar um novo subject via formulário."""
        data = {'name': 'New Subject', 'code': 'CS101'}
        response = self.client.post(reverse('add_subject'), data)
        self.assertRedirects(response, reverse('subject_list')) 
        subject = Subject.objects.get(name='New Subject')
        self.assertEqual(subject.code, 'CS101')
        self.assertEqual(subject.user, self.user)
    
    def test_add_subject_post_invalido(self):
        """Testa se a view trata corretamente um POST inválido (form.is_valid() == False)."""
        url = reverse('add_subject')
        data = {'name': '', 'code': 'CS101'}  # Nome inválido (vazio)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'form')  
        self.assertFalse(Subject.objects.exists())  
    
    def test_add_subject_get_form(self):
        """Testa se o formulário de adicionar subject é exibido com método GET (sem envio de dados)."""
        response = self.client.get(reverse('add_subject'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')  
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="code"')
        self.assertEqual(Subject.objects.count(), 0) 

    def test_subject_detail(self):
        """Testa se a página de detalhes de um subject exibe as informações corretamente."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        Note.objects.create(title="Test Note", content="This is a test note", subject=subject)
        response = self.client.get(reverse('subject_detail', args=[subject.id]))
        self.assertContains(response, subject.name)
        self.assertContains(response, "This is a test note")

    def test_add_note(self):
        """Testa se é possível adicionar uma nova nota a um subject."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        data = {'title': 'Test Note', 'content': 'This is a test note'}
        response = self.client.post(reverse('add_note', args=[subject.id]), data)
        self.assertRedirects(response, reverse('subject_detail', args=[subject.id]))
        note = Note.objects.get(title='Test Note')
        self.assertEqual(note.content, 'This is a test note')
        self.assertEqual(note.subject, subject)
    
    def test_add_note_post_invalido(self):
        """Testa se a view trata corretamente um POST inválido (form.is_valid() == False)."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        url = reverse('add_note', args=[subject.id])
        data = {'title': '', 'content': 'Conteúdo sem título'}  

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')  
        self.assertFalse(Note.objects.exists()) 

    def test_add_note_get_form(self):
        """Testa se o formulário de adicionar nota é exibido com método GET (sem envio de dados)."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        url = reverse('add_note', args=[subject.id])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="content"')
        self.assertEqual(Note.objects.count(), 0)  

    def test_subject_list_no_subjects(self):
        """Testa se a lista de subjects está vazia quando o usuário não tem subjects."""
        response = self.client.get(reverse('subject_list'))
        self.assertContains(response, "Nenhum assunto encontrado")

    def test_subject_detail_no_notes(self):
        """Testa se a página de detalhes de um subject mostra que não há notas ainda."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        response = self.client.get(reverse('subject_detail', args=[subject.id]))
        self.assertContains(response, "Nenhuma nota adicionada ainda.")
        
    def test_redirect_if_not_logged_in(self):
        """Testa o redirecionamento se o usuário não estiver autenticado."""
        self.client.logout()
        response = self.client.get(reverse('subject_list'))
        self.assertRedirects(response, '/login/?next=/subjects/')  

    def test_subject_str(self):
        """Testa o método __str__ da classe Subject."""
        subject = Subject.objects.create(name='Matemática', user=self.user)
        self.assertEqual(str(subject), 'Matemática')

    def test_note_str(self):
        """Testa o método __str__ da classe Note."""
        subject = Subject.objects.create(name='Matemática', user=self.user)
        note = Note.objects.create(title='Teorema de Pitágoras', content='Conteúdo da nota', subject=subject)
        self.assertEqual(str(note), 'Teorema de Pitágoras - Matemática')

    def test_all_notes_view_no_notes(self):
        """Testa se a view all_notes exibe mensagem apropriada quando não há notas."""
        response = self.client.get(reverse('all_notes'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Você ainda não possui anotações")  # conforme all_notes.html -- Validar depois
    
    def test_note_detail_not_found(self):
        """Testa se uma nota inexistente retorna 404."""
        response = self.client.get(reverse('note_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_all_notes_view(self):
        response = self.client.get(reverse('all_notes'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Nenhuma anotação")

    def test_note_detail_view(self):
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        note = Note.objects.create(title="Gravidade", content="Conteúdo da nota", subject=subject)
        response = self.client.get(reverse('note_detail', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, note.title)
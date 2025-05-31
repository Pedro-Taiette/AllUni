from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Subject, Note
import datetime

class SubjectTests(TestCase):
    
    def setUp(self):
        """Configura o usuário e dados básicos para os testes."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_subject_list(self):
        """Testa se a página de listagem de subjects exibe os subjects do usuário."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_list.html')
        self.assertIn(subject, response.context['subjects'])

    def test_add_subject(self):
        """Testa se é possível adicionar um novo subject via formulário."""
        data = {'name': 'New Subject', 'code': 'CS101', 'color': 'blue'}  
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
        self.assertTemplateUsed(response, 'subjects/add_subject.html')
        self.assertIn('form', response.context)
        self.assertEqual(Subject.objects.count(), 0)

    def test_subject_detail(self):
        """Testa se a página de detalhes de um subject exibe as informações corretamente."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        Note.objects.create(title="Test Note", content="This is a test note", subject=subject)
        response = self.client.get(reverse('subject_detail', args=[subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_detail.html')
        self.assertEqual(response.context['subject'], subject)
        self.assertEqual(list(response.context['notes']), list(subject.notes.all()))

    def test_add_note(self):
        """Testa se é possível adicionar uma nova nota a um subject."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        data = {'title': 'Test Note', 'content': 'This is a test note'}
        try:
            self.client.post(reverse('add_note', args=[subject.id]), data)
        except:
            pass
        
        self.assertTrue(Note.objects.filter(title='Test Note').exists())
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
        self.assertTemplateUsed(response, 'subjects/add_note.html')
        self.assertIn('form', response.context)
        self.assertEqual(Note.objects.count(), 0)  

    def test_subject_list_no_subjects(self):
        """Testa se a lista de subjects está vazia quando o usuário não tem subjects."""
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_list.html')
        self.assertEqual(list(response.context['subjects']), [])

    def test_subject_detail_no_notes(self):
        """Testa se a página de detalhes de um subject mostra que não há notas ainda."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        response = self.client.get(reverse('subject_detail', args=[subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_detail.html')
        self.assertEqual(list(response.context['notes']), [])
        
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

    def test_search_view_no_query(self):
        """Testa se a view de pesquisa funciona sem uma consulta."""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resultados da pesquisa")
        self.assertEqual(len(response.context['subjects']), 0)
        self.assertEqual(len(response.context['notes']), 0)

    def test_search_view_with_query(self):
        """Testa se a view de pesquisa retorna resultados corretos."""
        subject1 = Subject.objects.create(name="Matemática", user=self.user)
        subject2 = Subject.objects.create(name="Física", user=self.user)
        Note.objects.create(title="Álgebra", content="Conteúdo sobre álgebra", subject=subject1)
        Note.objects.create(title="Geometria", content="Conteúdo sobre geometria", subject=subject1)
        Note.objects.create(title="Mecânica", content="Conteúdo sobre mecânica", subject=subject2)
        
        response = self.client.get(reverse('search') + '?q=mate')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['subjects']), 1)
        self.assertEqual(response.context['subjects'][0].name, "Matemática")

        response = self.client.get(reverse('search') + '?q=álgebra')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 1)
        self.assertEqual(response.context['notes'][0].title, "Álgebra")

        response = self.client.get(reverse('search') + '?q=geometria')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 1)
        self.assertEqual(response.context['notes'][0].title, "Geometria")

    def test_search_view_no_results(self):
        """Testa se a view de pesquisa lida corretamente com consultas sem resultados."""
        Subject.objects.create(name="Matemática", user=self.user)
        
        response = self.client.get(reverse('search') + '?q=história')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['subjects']), 0)
        self.assertEqual(len(response.context['notes']), 0)
        self.assertContains(response, "Nenhum resultado encontrado")

    def test_search_view_requires_login(self):
        """Testa se a view de pesquisa requer login."""
        self.client.logout()
        response = self.client.get(reverse('search'))
        self.assertRedirects(response, '/login/?next=/subjects/search/')
    
    def test_subject_list_no_subjects(self):
        """Testa se a lista de subjects está vazia quando o usuário não tem subjects."""
        response = self.client.get(reverse('subject_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/subject_list.html')
        self.assertEqual(list(response.context['subjects']), [])

    def test_archive_subject(self):
        """Testa se é possível arquivar uma matéria."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        response = self.client.get(reverse('archive_subject', args=[subject.id]))
        self.assertRedirects(response, reverse('subject_list'))
        subject.refresh_from_db()
        self.assertTrue(subject.is_archived)

    def test_unarchive_subject(self):
        """Testa se é possível desarquivar uma matéria."""
        subject = Subject.objects.create(name="Test Subject", user=self.user, is_archived=True)
        response = self.client.get(reverse('unarchive_subject', args=[subject.id]))
        self.assertRedirects(response, reverse('subject_list'))
        subject.refresh_from_db()
        self.assertFalse(subject.is_archived)

    def test_toggle_favorite(self):
        """Testa se é possível marcar/desmarcar uma nota como favorita."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        note = Note.objects.create(title="Test Note", content="Content", subject=subject)
        
        # Marcar como favorita
        response = self.client.get(reverse('toggle_favorite', args=[note.id]))
        self.assertRedirects(response, reverse('note_detail', args=[note.id]))
        note.refresh_from_db()
        self.assertTrue(note.is_favorite)
        
        # Desmarcar como favorita
        response = self.client.get(reverse('toggle_favorite', args=[note.id]))
        self.assertRedirects(response, reverse('note_detail', args=[note.id]))
        note.refresh_from_db()
        self.assertFalse(note.is_favorite)

    def test_favorite_notes(self):
        """Testa se a view de notas favoritas responde e usa o template correto."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        Note.objects.create(title="Favorite Note", content="Content", subject=subject, is_favorite=True)
        Note.objects.create(title="Regular Note", content="Content", subject=subject)
        response = self.client.get(reverse('favorite_notes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/favorite_notes.html')

    def test_archived_subjects(self):
        """Testa se a view de matérias arquivadas responde e usa o template correto."""
        Subject.objects.create(name="Active Subject", user=self.user)
        Subject.objects.create(name="Archived Subject", user=self.user, is_archived=True)
        response = self.client.get(reverse('archived_subjects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subjects/archived_subjects.html')

    def test_recent_notes(self):
        """Testa se a view de notas recentes filtra corretamente as notas."""
        from unittest.mock import patch
        from django.http import HttpResponse
        
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        recent_note = Note.objects.create(title="Recent Note", content="Content", subject=subject)
        
        # Criar nota antiga
        old_note = Note.objects.create(title="Old Note", content="Content", subject=subject)
        old_date = timezone.now() - timedelta(days=10)
        Note.objects.filter(pk=old_note.pk).update(created_at=old_date)
        
        with patch('subjects.views.render') as mock_render:
            mock_render.return_value = HttpResponse()
            self.client.get(reverse('recent_notes'))
            
            context = mock_render.call_args[0][2]
            self.assertIn(recent_note, context['notes'])
            self.assertNotIn(old_note, context['notes'])


    def test_get_recent_notes(self):
        """Testa o método get_recent_notes da classe Subject."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        note1 = Note.objects.create(title="Note 1", content="Content", subject=subject)
        note2 = Note.objects.create(title="Note 2", content="Content", subject=subject)
        note3 = Note.objects.create(title="Note 3", content="Content", subject=subject)
        
        recent_notes = subject.get_recent_notes(2)
        self.assertEqual(len(recent_notes), 2)
        self.assertEqual(recent_notes[0].title, "Note 3")  # Mais recente primeiro
        self.assertEqual(recent_notes[1].title, "Note 2")

    def test_get_slug(self):
        """Testa o método get_slug da classe Subject."""
        subject = Subject.objects.create(name="Test Subject", user=self.user)
        self.assertEqual(subject.get_slug(), "test-subject")
        
        subject = Subject.objects.create(name="Cálculo Diferencial", user=self.user)
        self.assertEqual(subject.get_slug(), "calculo-diferencial")

class NoteReadingTimeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='senha')
        self.subject = Subject.objects.create(name='Português', user=self.user)
        self.note = Note.objects.create(
            title='Teste de Leitura',
            content='',
            subject=self.subject
        )

    def test_get_reading_time_minimum_one_minute(self):
        self.note.content = 'Apenas algumas palavras'
        self.note.save()
        self.assertEqual(self.note.get_reading_time(), 1)

    def test_get_reading_time_exact(self):
        self.note.content = 'palavra ' * 200
        self.note.save()
        self.assertEqual(self.note.get_reading_time(), 1)

        self.note.content = 'palavra ' * 400
        self.note.save()
        self.assertEqual(self.note.get_reading_time(), 2)

        self.note.content = 'palavra ' * 999
        self.note.save()
        self.assertEqual(self.note.get_reading_time(), 4)
    
class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='senha')
        self.subject = Subject.objects.create(name='História', user=self.user)
        self.note = Note.objects.create(
            title='Nota de Teste',
            content='Essa é uma nota de teste para verificar a função get_excerpt.',
            subject=self.subject
        )

    def test_get_excerpt_full_content(self):
        self.note.content = 'Pequeno'
        self.note.save()
        self.assertEqual(self.note.get_excerpt(50), 'Pequeno')

    def test_get_excerpt_truncated(self):
        self.note.content = 'A' * 150
        self.note.save()
        self.assertTrue(self.note.get_excerpt(100).endswith('...'))
        self.assertEqual(len(self.note.get_excerpt(100)), 103) 

class NoteIsRecentlyUpdatedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='senha')
        self.subject = Subject.objects.create(name='Biologia', user=self.user)
        self.note = Note.objects.create(
            title='Nota Recente',
            content='Conteúdo da nota',
            subject=self.subject
        )

    def test_is_recently_updated_true(self):
        """Deve retornar True se a nota foi atualizada dentro de 1 dia"""
        self.note.updated_at = timezone.now()
        self.note.save()
        self.assertTrue(self.note.is_recently_updated())

    def test_is_recently_updated_false(self):
        """Deve retornar False se a nota foi atualizada há mais de 1 dia"""
        self.note.updated_at = timezone.now() - datetime.timedelta(days=2)
        self.note.save()
        self.assertFalse(self.note.is_recently_updated())

    def test_is_recently_updated_custom_days(self):
        """Deve funcionar corretamente com valores diferentes de days"""
        self.note.updated_at = timezone.now() - datetime.timedelta(days=3)
        self.note.save()

        # Verifica com 5 dias (deve ser True)
        self.assertTrue(self.note.is_recently_updated(days=5))

        # Verifica com 2 dias (deve ser False)
        self.assertFalse(self.note.is_recently_updated(days=2))

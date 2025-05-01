from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):
    def setUp(self):
        # Cria um usuário para ser usado nos testes
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_register_get(self):
        """Deve carregar a página de registro com status 200.
        Testa a função register_view (GET), verificando se o formulário é carregado corretamente.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIn('form', response.context)

    def test_register_post_valido(self):
        """Deve registrar um novo usuário e redirecionar para login.
        Testa a função register_view (POST) com dados válidos. O usuário deve ser criado e o redirecionamento para o login deve ocorrer.
        """
        response = self.client.post(reverse('register'), {
            'username': 'novo',
            'password1': 'SenhaForte123',
            'password2': 'SenhaForte123',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='novo').exists())

    def test_register_post_invalido(self):
        """Não deve registrar com dados inválidos.
        Testa a função register_view (POST) com dados inválidos. O usuário não deve ser criado e erros de formulário devem ser mostrados.
        """
        response = self.client.post(reverse('register'), {
            'username': 'x',
            'password1': '123',
            'password2': '456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(User.objects.filter(username='x').exists())

    def test_login_get(self):
        """Deve carregar a página de login.
        Testa a função login_view (GET), verificando se a página de login é carregada corretamente.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")

    def test_login_post_sucesso(self):
        """Deve logar com sucesso e redirecionar para o dashboard.
        Testa a função login_view (POST) com dados válidos. O login deve ser bem-sucedido e o usuário redirecionado para o dashboard.
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_post_falha(self):
        """Deve falhar o login com credenciais erradas.
        Testa a função login_view (POST) com credenciais erradas. O login deve falhar e a mensagem de erro deve ser mostrada.
        """
        response = self.client.post(reverse('login'), {
            'username': 'errado',
            'password': 'senhaerrada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor")

    def test_logout(self):
        """Deve deslogar e redirecionar para login.
        Testa a função logout_view, verificando se o logout funciona corretamente e o redirecionamento para a página de login ocorre.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_dashboard_sem_login(self):
        """Usuário sem login deve ser redirecionado.
        Testa a função dashboard_view, verificando se um usuário não autenticado é redirecionado para a página de login.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_com_login(self):
        """Usuário autenticado deve acessar o dashboard.
        Testa a função dashboard_view, verificando se um usuário autenticado pode acessar a página do dashboard.
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/dashboard.html')

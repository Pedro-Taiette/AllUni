from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from users.views import register_view, dashboard_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

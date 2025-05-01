from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import users.views as views 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

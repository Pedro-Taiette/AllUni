from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.add_subject, name='add_subject'),
    path('notes/', views.all_notes, name='all_notes'), 
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'), 
    path('search/', views.search, name='search'),
    path('<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('<int:subject_id>/add_note/', views.add_note, name='add_note'),
]
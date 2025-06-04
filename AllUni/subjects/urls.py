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

    path('subjects/archived/', views.archived_subjects, name='archived_subjects'),
    path('subjects/<int:subject_id>/archive/', views.archive_subject, name='archive_subject'),
    path('subjects/<int:subject_id>/unarchive/', views.unarchive_subject, name='unarchive_subject'),

    path('notes/favorites/', views.favorite_notes, name='favorite_notes'),
    path('notes/<int:note_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('notes/recent/', views.recent_notes, name='recent_notes'),
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),

    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('tags/<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),
    path('tags/<int:tag_id>/notes/', views.tagged_notes, name='tagged_notes'),
]
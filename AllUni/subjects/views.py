from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Subject, Note, Tag, NoteTag
from .forms import SubjectForm, NoteForm, TagForm

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user, is_archived=False)
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def all_notes(request):
    notes = Note.objects.filter(subject__user=request.user)
    return render(request, 'subjects/all_notes.html', {'notes': notes})

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, subject__user=request.user)
    return render(request, 'subjects/note_detail.html', {'note': note})

@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/add_subject.html', {'form': form})

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    notes = subject.notes.all()
    
    return render(request, 'subjects/subject_detail.html', {
        'subject': subject,
        'notes': notes
    })

@login_required
def add_note(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    user_tags = Tag.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form_data = {
            'title': request.POST.get('title', ''),
            'content': request.POST.get('content', ''),
            'is_favorite': request.POST.get('is_favorite', False) == 'on'
        }
        
        if form_data['title'] and form_data['content']:
            note = Note.objects.create(
                title=form_data['title'],
                content=form_data['content'],
                is_favorite=form_data['is_favorite'],
                subject=subject
            )
            
            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id, user=request.user)
                    NoteTag.objects.create(note=note, tag=tag)
                except (Tag.DoesNotExist, ValueError):
                    pass
                
            return redirect('subject_detail', subject_id=subject.id)
        else:
            form = NoteForm(form_data)
    else:
        form = NoteForm()
            
    return render(request, 'subjects/add_note.html', {
        'form': form, 
        'subject': subject,
        'user_tags': user_tags
    })

@login_required
def edit_note(request, note_id):
    """Edita uma nota existente."""
    note = get_object_or_404(Note, id=note_id, subject__user=request.user)
    user_tags = Tag.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form_data = {
            'title': request.POST.get('title', ''),
            'content': request.POST.get('content', ''),
            'is_favorite': request.POST.get('is_favorite') == 'on'
        }
        
        if form_data['title'] and form_data['content']:
            note.title = form_data['title']
            note.content = form_data['content']
            note.is_favorite = form_data['is_favorite']
            note.save()
            
            NoteTag.objects.filter(note=note).delete()  # Remove todas as tags existentes
            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id, user=request.user)
                    NoteTag.objects.create(note=note, tag=tag)
                except (Tag.DoesNotExist, ValueError):
                    pass
                    
            return redirect('note_detail', note_id=note.id)
        else:
            form = NoteForm(form_data, instance=note)
    else:
        form = NoteForm(instance=note)
    
    current_tags = note.tags.all()
    
    return render(request, 'subjects/edit_note.html', {
        'form': form, 
        'note': note,
        'user_tags': user_tags,
        'current_tags': current_tags
    })

@login_required
def search(request):
    query = request.GET.get('q', '')
    subjects = []
    notes = []
    tags = []
    
    if query:
        subjects = Subject.objects.filter(
            user=request.user,
            name__icontains=query
        )
        
        notes = Note.objects.filter(
            subject__user=request.user
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        
        tags = Tag.objects.filter(
            user=request.user,
            name__icontains=query
        )
    
    return render(request, 'subjects/search_results.html', {
        'query': query,
        'subjects': subjects,
        'notes': notes,
        'tags': tags,
    })

@login_required
def favorite_notes(request):
    """Exibe apenas as notas favoritas do usuário."""
    notes = Note.objects.filter(subject__user=request.user, is_favorite=True).order_by('-created_at')
    return render(request, 'subjects/favorite_notes.html', {'notes': notes})

@login_required
def archive_subject(request, subject_id):
    """Arquiva uma matéria."""
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.is_archived = True
    subject.save()
    return redirect('subject_list')

@login_required
def unarchive_subject(request, subject_id):
    """Desarquiva uma matéria."""
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.is_archived = False
    subject.save()
    return redirect('subject_list')

@login_required
def toggle_favorite(request, note_id):
    """Marca/desmarca uma nota como favorita."""
    note = get_object_or_404(Note, id=note_id, subject__user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect('note_detail', note_id=note.id)

@login_required
def archived_subjects(request):
    """Exibe matérias arquivadas."""
    subjects = Subject.objects.filter(user=request.user, is_archived=True)
    return render(request, 'subjects/archived_subjects.html', {'subjects': subjects})

@login_required
def recent_notes(request):
    """Exibe notas recentes."""
    from django.utils import timezone
    import datetime
    recent_date = timezone.now() - datetime.timedelta(days=7)
    notes = Note.objects.filter(subject__user=request.user, created_at__gte=recent_date)
    return render(request, 'subjects/recent_notes.html', {'notes': notes})

@login_required
def tag_list(request):
    """Lista todas as tags do usuário."""
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'subjects/tag_list.html', {'tags': tags})

@login_required
def add_tag(request):
    """Adiciona uma nova tag."""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'subjects/add_tag.html', {'form': form})

@login_required
def delete_tag(request, tag_id):
    """Exclui uma tag."""
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    tag.delete()
    return redirect('tag_list')

@login_required
def tagged_notes(request, tag_id):
    """Exibe notas com uma tag específica."""
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    notes = Note.objects.filter(notetag__tag=tag)
    return render(request, 'subjects/tagged_notes.html', {'notes': notes, 'tag': tag})

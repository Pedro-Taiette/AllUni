from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from subjects.models import Subject, Note 

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard_view(request):
    subject_count = Subject.objects.filter(user=request.user).count()
    note_count = Note.objects.filter(subject__user=request.user).count()

    recent_subjects = Subject.objects.filter(
        user=request.user,
        is_archived=False
    ).order_by('-created_at')[:3]

    context = {
        'subject_count': subject_count,
        'note_count': note_count,
        'recent_subjects': recent_subjects,
    }
    return render(request, 'users/dashboard.html', context)
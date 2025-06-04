from django.contrib import admin
from subjects.models import Subject, Note, Tag, NoteTag

admin.site.register(Subject)
admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(NoteTag)


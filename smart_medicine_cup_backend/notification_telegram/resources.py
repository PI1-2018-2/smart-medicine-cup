# api/resources.py
from tastypie.resources import ModelResource
from notification_telegram.models import Note

class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
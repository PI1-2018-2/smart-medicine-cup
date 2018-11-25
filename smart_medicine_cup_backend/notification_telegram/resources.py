# api/resources.py
from tastypie.resources import ModelResource
from .models import Note

class NotificationResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'notification'
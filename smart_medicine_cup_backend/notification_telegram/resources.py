# api/resources.py
from tastypie.resources import ModelResource
from cups.models import Record

class NotificationResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'notification'
# api/resources.py
from tastypie.resources import ModelResource
from cups.models import Record
from tastypie.authorization import Authorization

class NotificationResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'notification'
        authorization = Authorization()
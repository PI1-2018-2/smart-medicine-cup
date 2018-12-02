from tastypie.resources import ModelResource
from smc.models import Record
class RecordResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'
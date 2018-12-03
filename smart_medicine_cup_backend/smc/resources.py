from tastypie.resources import ModelResource
from smc.models import Record, Cup

class RecordResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'

class CupResource(ModelResource):
    class Meta:
        queryset = Cup.objects.all()
        resource_name = 'cup'

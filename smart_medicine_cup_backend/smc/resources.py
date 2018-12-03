from tastypie.resources import ModelResource
from smc.models import Record, Contact, Cup

class RecordResource(ModelResource):
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'


class ContactResource(ModelResource):
    class Meta:
        queryset = Contact.objects.select_related('user')
        resource_name = 'contact'
# Django imports
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Local Django imports
from models import Record, Cups


class ListRecords(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'list_record'
    model = Record
    paginate_by = 20

    def dispatch(self, *args, **kwargs):
        return super(ListRecords, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        cups_id = self.get_cups_id() 
        return self.model.objects.filter(cup_id=cups_id)

    def get_cups_id(self):
        return self.Cups.objects.filter(user_id=self.request.user))
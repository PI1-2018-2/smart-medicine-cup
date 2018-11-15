# Django imports
from django.views.generic import ListView
from django.utils.decorators import method_decorator

# Local Django imports
from cups.models import Cup

class ListCups(ListView):
    '''
        View for list created of health professional in database.
    '''
    template_name = 'list_cups.html'
    context_object_name = 'list_cups'
    model = Cup 
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(ListPatterns, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_creator=self.request.user)
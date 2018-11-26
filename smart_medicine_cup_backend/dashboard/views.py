from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.utils.decorators import method_decorator

# Local Django imports
from cups.models import Cup,Record

class Dashboard(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'list_record'
    model = Record 
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        #return self.model.objects.filter(user_creator=self.request.user)
        print(self.model.objects.all())
        return self.model.objects.all()

class EditRegistration(TemplateView):
    template_name = "edit_registration.html"

class Login(TemplateView):
    template_name = "login.html"

class AddSmc(TemplateView):
    template_name = "addsmc.html"

class Smc(ListView):
    template_name = "smc.html"
    context_object_name = 'list_cups'
    model = Cup
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Smc, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        print(self.model.objects.all())
        return self.model.objects.filter(user=self.request.user)

class Historic(ListView):
    template_name = "historic.html"
    context_object_name = 'list_record'
    model = Record 
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Historic, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        query = Cup.objects.filter(user=self.request.user)
        print(self.model.objects.all())
        return self.model.objects.all()

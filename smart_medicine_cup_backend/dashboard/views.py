from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from smc.models import Contact, Cup, Record

# Create your views here.
class Dashboard(TemplateView):
    template_name = "dashboard.html"

class EditRegistration(TemplateView):
    template_name = "edit_registration.html"

class Login(TemplateView):
    template_name = "login.html"

class Smc(ListView):
    template_name = "smc.html"
    context_object_name = 'list_smc'
    model = Cup

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class Historic(ListView):
    template_name = "historic.html"
    context_object_name = 'list_historic'
    model = Record

    def get_queryset(self):
        return self.model.objects.all()

class Contacts(ListView):
    template_name = "contacts.html"
    context_object_name = 'list_contacts'
    model = Contact

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

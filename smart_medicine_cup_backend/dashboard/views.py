from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from smc.models import Cup, Record, Alarm

# Create your views here.
class Dashboard(View):
    template_name = "dashboard.html"

    def get(self, request):
        list_smc = Cup.objects.filter(user=self.request.user)
        list_historic = Record.objects.filter(alarm__cup__user=self.request.user)
        return render(request, self.template_name, {'list_smc': list_smc,
                                                    'list_historic': list_historic})

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
        return self.model.objects.filter(alarm__cup__user=self.request.user)

class Alarms(ListView):
    template_name = "alarms.html"
    model = Alarm
    context_object_name = 'list_alarm'

    def get_queryset(self):
        return self.model.objects.filter(cup__user=self.request.user)

from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Dashboard(TemplateView):
    template_name = "dashboard.html"

class Registration(TemplateView):
    template_name = "registration.html"

class EditRegistration(TemplateView):
    template_name = "edit_registration.html"

class Login(TemplateView):
    template_name = "login.html"

class Smc(TemplateView):
    template_name = "smc.html"

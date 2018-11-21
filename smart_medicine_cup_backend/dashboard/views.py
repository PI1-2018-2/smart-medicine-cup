from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Dashboard(TemplateView):
    template_name = "dashboard.html"

class EditRegistration(TemplateView):
    template_name = "edit_registration.html"

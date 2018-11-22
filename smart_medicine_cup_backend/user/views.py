from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Login(TemplateView):
    template_name = "login.html"

class SingUp(TemplateView):
	template_name = "signup.html"
    

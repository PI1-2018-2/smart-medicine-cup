from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from smc.models import Cup
from ..forms.user import SignUpForm


def add_smc(request):
    if request.method == 'POST':
        code = request.POST.get('smcCode')
        username = request.POST.get('username')
        Cup.objects.create(cup_id=code, user=request.user, username=username)
        return redirect('/dashboard/smc')

# def add_contact(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         Contact.objects.create(username=username, user=request.user)
#         return redirect('/dashboard/contacts')
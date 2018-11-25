from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from ..forms.user import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard/'))
            else:
                print('Error login')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('/'))

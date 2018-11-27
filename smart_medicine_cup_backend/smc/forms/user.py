from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), label='Nome de usuário', error_messages={'required': 'Por favor, informe um nome que será usado no login.', 'max_length': 'Por favor, escolher um nome menor.'})
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), label='Nome')
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), label='Sobrenome')
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}), label='E-mail')
    password1 = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}), label='Senha')
    password2 = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}), label='Confirmar senha')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

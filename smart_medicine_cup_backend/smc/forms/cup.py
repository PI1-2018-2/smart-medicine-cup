from django import forms
from models import Cup


class RegistrationCup():
    code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), label='Código do Copo', error_messages={'required': 'Por favor, informe o código do seu SMC.'})
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), label='Nome do Contato', error_messages={'required': 'Por favor, informe o nome do seu contato para o SMC.'})
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}), label='Telefone do Contato', error_messages={'required': 'Por favor, informe o número do seu contato para o SMC.'})
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}), label='Email do Contato', error_messages={'required': 'Por favor, informe o emails do seu contato para o SMC.'})

    class Meta:
        model = Cup
        fields = ('code', 'name', 'phone', 'email')

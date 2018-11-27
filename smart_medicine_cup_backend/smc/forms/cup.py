from django import forms
from models import Cup


class RegistrationCup():
    code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), label='Código do Copo', error_messages={'required': 'Por favor, informe o código do seu SMC.'})

    class Meta:
        model = Cup
        fields = ('code')

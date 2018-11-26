from django import forms
from .models import Cup, Contact

class CupForm(forms.ModelForm):
    cup_id = forms.CharField()
    
    class Meta:
        model = Cup
        fields = ['cup_id']

class ContactForm(forms.ModelForm):
    name = forms.CharField()
    username = forms.CharField()
    
    class Meta:
        model = Contact
        fields = ['name','username']
from django import forms
from .models import Cup
class CupForm(forms.ModelForm):
    cup_id = forms.CharField()
    
    class Meta:
        model = Cup
        fields = ['cup_id']
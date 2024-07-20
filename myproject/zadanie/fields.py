from django import forms

from .models import Zadanie

class ProduktForm(forms.ModelForm):
    class Meta:
        model = Zadanie
        fields = [
            'nazwa',
            'opis',
            'status'
        ]
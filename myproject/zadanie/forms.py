from django import forms
from .models import Zadanie
from django.contrib.auth.models import User

class ZadanieForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    przypisany_uzytkownik = forms.ModelChoiceField(queryset=User.objects.all(), required=False, empty_label="Brak użytkownika")
    class Meta:
        model = Zadanie
        fields = ['id', 'nazwa', 'opis', 'status', 'przypisany_uzytkownik']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ZadanieForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id'].initial = self.instance.pk
        else:
            self.fields['id'].widget = forms.HiddenInput()
        if user and not user.has_perm('zadanie.can_edit_all_tasks'):
            self.fields['przypisany_uzytkownik'].widget = forms.HiddenInput()

class ZadanieFilterForm(forms.Form):
    id = forms.IntegerField(required=False, label='ID')
    nazwa = forms.CharField(required=False, label='Nazwa')
    opis = forms.CharField(required=False, label='Opis')
    status = forms.ChoiceField(choices=[('', 'Wybierz status')] + list(Zadanie.STATUS_CHOICES), required=False, label='Status')
    uzytkownik = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Użytkownik')

from django import forms
from .models import RendezVous

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['nom','prenom','CIN','telephone', 'email' ,'date', 'time','presence']

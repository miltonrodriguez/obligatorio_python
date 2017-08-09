from django import forms
from .models import Socio

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ("documento","nombre","email","fecha_nacimiento")
        
from django import forms
from .models import Socio, Libro, Ejemplar

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ("documento","nombre","email","fecha_nacimiento")
        

class PrestamoForm(forms.Form):
    libro = forms.ModelChoiceField(queryset=Libro.objects.all())
    socio = forms.ModelChoiceField(queryset=Socio.objects.all())
    
class DevolucionForm(forms.Form):
    ejemplar = forms.ModelChoiceField(queryset=Ejemplar.objects.all())
    socio = forms.ModelChoiceField(queryset=Socio.objects.all())
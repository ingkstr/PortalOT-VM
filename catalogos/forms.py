from django import forms
from catalogos.models import AgenteCorreo

class AgenteCorreoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AgenteCorreo
        fields = {'correo','password'}

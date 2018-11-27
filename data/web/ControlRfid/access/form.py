from django import forms
from .models import Zona, Evento, Ambiente

class PostZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ('fechadura', 'etiqueta')

class PostAmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = ('fechadura', 'ambiente', 'descri')



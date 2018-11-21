from django import forms
from .models import Zona

class PostForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ('fechadura', 'etiqueta')

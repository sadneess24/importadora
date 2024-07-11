from django import forms
from .models import *

class ReseniaFormulario(forms.ModelForm):
    class Meta:
        model = CalificacionResenia
        fields = ['sujeto','resenia','calificacion']
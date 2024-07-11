from django import forms
from .models import *

class FormularioOrden(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','pais','region','comuna','nota_orden']
from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *

class RegistroFormulario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingresa tu contraseña',
        'class':'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirma tu contraseña',
        'class':'form-control'
    }))
    class Meta:
        model = Cuenta
        fields = ['first_name','last_name','phone_number','email','password']
        
    def __init__(self, *args, **kwargs):
        super(RegistroFormulario, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingresa tu nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingresa tu apellido'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingresa tu telefono'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingresa tu correo electronico'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(RegistroFormulario,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "La contraseña no es igual"
            )
from typing import Any
from django.forms import (
    Form,
    TextInput,
    EmailInput,
    CharField,
    PasswordInput
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class FormularioRegistro(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Contraseña'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirmar contraseña'}

    class Meta:
        model = User
        fields = (
            'username', 
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
            )
        widgets = {
            'username': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre de usuario'
                }
            ),
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre'
                },
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellido'
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico'
                }
            ),
        }

class FormularioEntrar(Form):
    username = CharField(
        required=True,
        label='Nombre de usuario',
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }
        )
    )
    password = CharField(
        required = True,
        label = 'Contraseña',
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )

class FormularioEditar(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nombre'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Apellido'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo electrónico'
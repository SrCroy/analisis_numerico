from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')
    carrera = forms.CharField(max_length=100)
    carnet = forms.CharField(max_length=20)
    ciclo = forms.CharField(max_length=20)
    fotografia = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")
        if password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

class LoginForm(forms.Form):
    correo = forms.CharField(label='Correo')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

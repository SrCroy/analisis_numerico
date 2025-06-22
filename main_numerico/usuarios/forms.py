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

class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)
    password = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput, required=False)
    confirmar_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = PerfilUsuario
        fields = ['fotografia', 'carrera', 'carnet', 'ciclo']
        widgets = {
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'carnet': forms.TextInput(attrs={'class': 'form-control'}),
            'ciclo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")
        if password or confirmar:
            if password != confirmar:
                raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    fotografia = forms.ImageField(
        label='Foto de perfil',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

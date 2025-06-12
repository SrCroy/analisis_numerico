from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contrasena']
        widgets = {
            'contrasena': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar = cleaned_data.get("confirmar_contrasena")

        if contrasena != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden")

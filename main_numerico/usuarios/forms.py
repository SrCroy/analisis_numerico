from django import forms
from .models import Usuario
import sympy as sp


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


class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    contrasena = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")



class DiferenciacionForm(forms.Form):
    f = forms.CharField(label='Escriba la ecuacion:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: x**2+5*3x'}))
    x = forms.CharField(label='Ingrese el valor de X:', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 7'}))
    h = forms.CharField(label='Ingrese el valor de h', widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 0.4'}))

    def clean_f(self):
        f_value = self.cleaned_data['f']
        try:
            sp.sympify(f_value)
        except SyntaxError:
            raise forms.ValidationError('La ecuación ingresada no es válida.')

        return f_value

    def clean_x(self):
        x_value = self.cleaned_data['x']
        try:
            float(x_value)
        except ValueError:
            raise forms.ValidationError('Ingrese un valor numérico válido para X.')

        return x_value

    def clean_h(self):
        h_value = self.cleaned_data['h']
        try:
            float(h_value)
        except ValueError:
            raise forms.ValidationError('Ingrese un valor numérico válido para h.')

        return h_value

    def clean(self):
        cleaned_data = super().clean()
        x_value = cleaned_data.get('x')
        h_value = cleaned_data.get('h')

        if x_value and h_value:
            x_float = float(x_value)
            h_float = float(h_value)

            if h_float == 0:
                raise forms.ValidationError('El valor de h no puede ser cero.')

        return cleaned_data

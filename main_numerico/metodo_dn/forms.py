from django import forms
from .models import DifferenceDividedHistory

class DifferenceDividedHistoryForm(forms.ModelForm):
    class Meta:
        model = DifferenceDividedHistory
        fields = ['function', 'x_value', 'h_value']
        widgets = {
            'function': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ejemplo: x**2 + 3*x',
                'rows': 2
            }),
            'x_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ingrese el valor de x'
            }),
            'h_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ingrese el valor de h'
            }),
        }
        labels = {
            'function': 'Función',
            'x_value': 'Valor de x',
            'h_value': 'Valor de h (incremento)',
        }

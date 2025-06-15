from django import forms

class DatosNewtonForm(forms.Form):
    x_valores = forms.CharField(
        label='Valores de x (separados por coma)',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 1, 2, 3'})
    )
    y_valores = forms.CharField(
        label='Valores de y (separados por coma)',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 2, 4, 6'})
    )
    valor_evaluar = forms.FloatField(
        label='Valor de x a evaluar (opcional)',
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej: 2.5'})
    )

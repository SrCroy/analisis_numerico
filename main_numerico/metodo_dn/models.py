from django.db import models
from django.contrib.auth.models import User

class DifferenceDividedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='differentiation_histories')
    function = models.TextField(help_text="Función matemática en formato de texto, ej. 'x**2 + 3*x'")
    x_value = models.FloatField(verbose_name="Valor de x")
    h_value = models.FloatField(verbose_name="Valor de h (incremento)")

    # Resultados de derivadas
    derivada_forward = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    derivada_backward = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    derivada_central = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    derivada_exacta = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)

    # Fórmulas y pasos
    formula_forward = models.TextField(blank=True)
    pasos_forward = models.TextField(blank=True)

    formula_backward = models.TextField(blank=True)
    pasos_backward = models.TextField(blank=True)

    formula_central = models.TextField(blank=True)
    pasos_central = models.TextField(blank=True)

    # Errores
    error_forward = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    error_backward = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    error_central = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Diferenciación"
        verbose_name_plural = "Historiales de Diferenciación"
        ordering = ['-created_at']

    def __str__(self):
        return f"Historial de {self.user.username} ({self.created_at.strftime('%d-%m-%Y %H:%M:%S')})"

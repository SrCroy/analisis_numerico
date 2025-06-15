from django.db import models

class HistorialNewton(models.Model):
    usuario_id = models.IntegerField()
    usuario_nombre = models.CharField(max_length=100)
    puntos_x = models.TextField()
    puntos_y = models.TextField()
    polinomio = models.TextField()
    valor_evaluado = models.FloatField(null=True, blank=True)  # Permitir nulos
    resultado = models.FloatField(null=True, blank=True)       # Permitir nulos
    pasos = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario_nombre} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"

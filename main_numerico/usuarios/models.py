from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class DifferenceDividedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    function = models.CharField(max_length=255)
    x_value = models.FloatField()
    h_value = models.FloatField()
    derivada_fwd = models.FloatField()
    formula_fwd = models.TextField()
    pasos_fwd = models.TextField()
    derivada_bwd = models.FloatField()
    formula_bwd = models.TextField()
    pasos_bwd = models.TextField()
    derivada_cen = models.FloatField()
    formula_cen = models.TextField()
    pasos_cen = models.TextField()
    derivada_exacta = models.FloatField()
    error_fwd = models.FloatField()
    error_bwd = models.FloatField()
    error_cen = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

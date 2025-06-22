from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fotografia = models.ImageField(
        upload_to='fotos_perfil/',
        null=True,
        blank=True,
        default='fotos_perfil/default.png'  # Debes tener esta imagen en tu carpeta media
    )
    carrera = models.CharField(max_length=100)
    carnet = models.CharField(max_length=20)
    ciclo = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.carrera})'

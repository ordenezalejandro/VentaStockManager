from django.db import models
from django.contrib.auth.models import User

class Vendedor(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # nombre = models.TextField()
    # apellido = models.TextField(blank=False)
    # perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    cuil = models.IntegerField(blank=False)
    telefono = models.TextField(blank=False)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=GENERO_CHOICES)

  # Campos adicionales del vendedor (opcional)
  # Ej: nombre_completo, telefono, etc.

    def __str__(self):

        return self.usuario.username
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"# Create your models here.

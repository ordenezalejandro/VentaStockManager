from django.db import models
from django.contrib.auth.models import User

class Vendedor(models.Model):
    GENERO_CHOICES = [ 
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.TextField()
    apellido = models.TextField(blank=False)
    # perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    cuil = models.IntegerField(blank=False)
    telefono = models.TextField(blank=False)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=GENERO_CHOICES)

  # Campos adicionales del vendedor (opcional)
  # Ej: nombre_completo, telefono, etc.
    def fullname(self):
            return self.nombre + ' ' + self.apellido

    def __str__(self):
        return self.usuario.username
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"# Create your models here.

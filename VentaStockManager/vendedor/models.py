from django.db import models
from django.contrib.auth.models import User
import re

def validar_cuil(cuil):
    """
    Validar un CUIL Argentino.
    El CUIL debe tener 11 dígitos.
    """
    # Regex para verificar el formato correcto
    if not re.match(r'^\d{2}-\d{8}-\d$', cuil):
        return False
    
    # Remover los guiones
    cuil = cuil.replace('-', '')

    # Coeficientes para validación
    coef = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    suma = 0

    for i in range(10):
        suma += int(cuil[i]) * coef[i]

    digito_verificador = (11 - (suma % 11)) % 11
    return digito_verificador == int(cuil[-1])

# Ejemplo de uso:
# print(validar_cuil("20-12345678-9"))

def validate_cuil(value):
    if not validar_cuil(value):
        raise ValidationError(f'{value} no es un CUIL válido')
    
class Vendedor(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.TextField()
    apellido = models.TextField(blank=True, null=True)
    # perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.TextField(blank=True, null=True)
    
  # Campos adicionales del vendedor (opcional)
  # Ej: nombre_completo, telefono, etc.
    def fullname(self):
            return self.nombre + ' ' + self.apellido

    def __str__(self):
        return self.usuario.username
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"# Create your models here.


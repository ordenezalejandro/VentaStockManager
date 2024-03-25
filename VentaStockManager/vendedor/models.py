from django.db import models

from django.contrib.auth.models import User, Group

# Crea un grupo de vendedores
import django

# django.setup()
# group, created = Group.objects.get_or_create(name='Vendedores', created=True)
# Create your models here.
class Vendedor(models.Model):
    # ... define los campos específicos del vendedor

    # Relación con el usuario (opcional)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username  # O el nombre que prefieras


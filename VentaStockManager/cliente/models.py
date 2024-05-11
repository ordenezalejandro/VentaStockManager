# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver



class Cliente(models.Model):
    """
    A model representing a client.
    """
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    nombre = models.TextField()
    apellido = models.TextField(blank=False)
    perfil = models.OneToOneField(User, on_delete=models.CASCADE)
    cuil = models.IntegerField(blank=False)
    telefono = models.TextField(blank=False)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=GENERO_CHOICES)


    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def clean(self):
        """
        Clean method to validate the client's age.
        """
        if self.edad <= 0:
            raise ValidationError("La edad debe ser mayor a 0")
    class Meta:
        """
        Meta class for the Cliente model.
        """
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

        # def get_latest_by(self):
        #     pass

        # def get_ordering(self):
        #     pass

    def __str__(self):
        return self.nombre + "  " + self.apellido + f" ({self.edad} años)"

    def get_absolute_url(self):
        """
        Get the absolute URL for the client detail view.
        """
        return reverse("cliente_detail", kwargs={"pk": self.pk})
    
        
#Permission.objects.create(
#   codename='puede_acceder_lista_articulos',  
#   name='Puede acceder a la lista de artículos'   





# # Obtén el grupo de usuarios o créalo si no existe
# clientes_group, created = Group.objects.get_or_create(name='Clientes')

# # Obtén el permiso o créalo si no existe
# permission, created = Permission.objects.get_or_create(
#     codename='puede_acceder_lista_articulos',  
#     name='Puede acceder a la lista de artículos'
# )

# # Agrega el permiso al grupo de usuarios
# clientes_group.permissions.add(permission)



# # Obtén el grupo de usuarios o créalo si no existe
# clientes_group, created = Group.objects.get_or_create(name='Clientes')

# # Obtén el permiso o créalo si no existe
# permission, created = Permission.objects.get_or_create(
#     codename='puede_acceder_lista_articulos',  
#     name='Puede acceder a la lista de artículos'
# )

# # Agrega el permiso al grupo de usuarios
# clientes_group.permissions.add(permission)

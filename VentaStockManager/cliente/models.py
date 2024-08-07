# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Cliente(models.Model):
    """
    A model representing a client.
    """
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    nombre = models.TextField(blank=False)
    apellido = models.TextField(blank=False)
    telefono = models.TextField(default='00000000', blank=True, null=True)
    direccion = models.CharField(max_length=50, default='direccion', blank=True, null=True)
    codigo_interno = models.CharField(max_length=50, default='no-codigo', blank=True, null=True)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_str_with_user(self, user):
        if user.is_superuser:
            return f"{self.nombre} {self.apellido} - {self.direccion}"
        return str(self)
    # def clean(self):
    #     """       
    #     Clean method to validate the client's age.
    #     """
    #     if self.edad and self.edad <= 0:
    #         raise ValidationError("La edad debe ser mayor a 0")
        
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
        return self.nombre + "  " + self.apellido + f" ({self.direccion})" if self.direccion else "(sin direccion)"

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

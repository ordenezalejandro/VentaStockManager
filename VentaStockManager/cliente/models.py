# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

        # def get_latest_by(self):
        #     pass

        # def get_ordering(self):
        #     pass

    def __str__(self):
        return f"Cliente:" + self.nombre + "  " + self.apellido + f" ({self.edad} años)"

    def get_absolute_url(self):
        """
        Get the absolute URL for the client detail view.
        """
        return reverse("Cliente_detail", kwargs={"pk": self.pk})

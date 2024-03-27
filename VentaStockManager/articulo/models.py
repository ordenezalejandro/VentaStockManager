import random
import string

from django.db import models

class Articulo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.PositiveIntegerField()
    codigo_interno = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    precio_minorista = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayorista = models.DecimalField(max_digits=10, decimal_places=2)
    vencimiento = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo_interno:
            # Obtener las iniciales del nombre del artículo
            iniciales = ''.join(word[0] for word in self.nombre.split())
            # Generar un número aleatorio de 4 dígitos
            random_number = ''.join(random.choices(string.digits, k=4))
            # Combinar las iniciales y el número aleatorio
            self.codigo_interno = iniciales.upper() + random_number
        super().save(*args, **kwargs)


    def __str__(self):
        return self.nombre


class ArticuloAutocomplete(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
from django.db import models

class Articulo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.PositiveIntegerField()
    codigo_interno = models.CharField(max_length=50, blank=True, null=True)  # Nuevo campo para el código interno
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    precio_minorista = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayorista = models.DecimalField(max_digits=10, decimal_places=2)
    vencimiento = models.DateField(blank=True)

    def __str__(self):
        return self.nombre

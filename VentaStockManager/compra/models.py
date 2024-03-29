from django.db import models
from articulo.models import Articulo

class Proveedor(models.Model):
    """Modelo que representa un proveedor"""
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

# class ArticuloCompra(models.Model):
#     """Modelo que representa un artículo de compra"""
#     nombre = models.CharField(max_length=255)
#     descripcion = models.TextField(blank=True)
#     precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.nombre

class Compra(models.Model):
    """Modelo que representa una compra"""
    fecha_compra = models.DateField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    articulos = models.ManyToManyField(Articulo, through='DetalleCompra')

    def __str__(self):
        return f"Compra del {self.fecha_compra} al proveedor {self.proveedor}"

class DetalleCompra(models.Model):
    """Modelo que representa el detalle de una compra"""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update stock of the related ArticuloCompra
        self.articulo.stock += self.cantidad  # Assuming a stock field in ArticuloCompra
        self.articulo.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.cantidad} unidades de {self.articulo} en la compra {self.compra}"
    
 
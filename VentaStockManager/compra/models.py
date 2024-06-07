from django.db import models
from articulo.models import Articulo
from django.contrib.auth.models import User

class Proveedor(models.Model):
    """Modelo que representa un proveedor"""
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, default='direccion Vacia', blank=True, null=True)
    telefono = models.CharField(max_length=20, default='0000000', blank=True, null=True)
    

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


    def __str__(self):
        return f"Compra del {self.fecha_compra} al proveedor {self.proveedor}"

class DetalleCompra(models.Model):
    """Modelo que representa el detalle de una compra"""
    compra = models.ForeignKey(Compra, related_name="detalles_compra", on_delete=models.CASCADE)
    articulo  = models.ForeignKey(Articulo, related_name="articulos_comprados", on_delete=models.CASCADE)   
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update stock of the related ArticuloCompra
        self.articulo.stock += self.cantidad  # Assuming a stock field in ArticuloCompra
        self.articulo.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.cantidad} unidades de {self.articulo} en la compra {self.compra}"
    
 
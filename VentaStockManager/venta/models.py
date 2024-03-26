from django.db import models

# Create your models here.
from django.db import models
from cliente.models import Cliente
from articulo.models import Articulo
# from vendedor.models import Vendedor
from vendedor.models import Vendedor


class Venta(models.Model):
    fecha_compra = models.DateField()
    fecha_entrega = models.DateField()
    cliente = models.ForeignKey(Cliente, related_name='ventas', on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, related_name='ventas', on_delete=models.CASCADE)
    @property
    def precio_total(self):
        return sum([articulo.precio for articulo in self.articulos_ventdidos.all()])

class ArticuloVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='ventas', on_delete=models.CASCADE)
    articulo =  models.ForeignKey(Articulo, related_name='articulos_ventdidos', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField()
    precio_minorista = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayorista = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Update stock of the related ArticuloCompra
        self.articulo.stock -= self.cantidad  # Assuming a stock field in ArticuloCompra
        self.articulo.save()
        super().save(*args, **kwargs)
        
         
    def __str__(self):
        return f"{self.cantidad} unidades de {self.articulo} en la venta {self.venta}"
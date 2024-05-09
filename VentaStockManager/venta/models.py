from django.db import models

# Create your models here.
from django.db import models
from cliente.models import Cliente
from articulo.models import Articulo
# from vendedor.models import Vendedor
from vendedor.models import Vendedor
from django.utils.translation import gettext_lazy as _



class Venta(models.Model):
    fecha_compra = models.DateField()
    fecha_entrega = models.DateField()
    cliente = models.ForeignKey(Cliente, related_name='ventas', on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, related_name='ventas', on_delete=models.CASCADE)
    class Meta:
        ordering = ['fecha_compra']
        verbose_name = _("venta")
        verbose_name_plural = _("ventas")


    def __str__(self):
        return f"Venta del {self.fecha_compra} al cliente {self.cliente}"
    
    @property
    def precio_total(self):
        if not self.ventas.exists():
            return 0
        return sum([articulo.precio for articulo in self.articulos_ventdidos.all()])

class ArticuloVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='ventas', on_delete=models.CASCADE)
    articulo =  models.ForeignKey(Articulo, related_name='articulos_ventdidos', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    precio = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        # Update stock of the related ArticuloCompraπ
        self.articulo.stock -= self.cantidad  # Assuming a stock field in ArticuloCompra
        self.articulo.save()
        super().save(*args, **kwargs)

    def get_precio_total(self):
        if self.articulo:
            return self.cantidad * self.articulo.price
        else:
            return 0
    @property
    def precio_minorista_2(self):
        return str(self.articulo.precio_minorista)

    @property
    def total(self):

        return self.cantidad * self.articulo.price

    def __str__(self):
        return f"{self.cantidad} unidades de {self.articulo} en la venta {self.venta}"
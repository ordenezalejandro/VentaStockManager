from typing import Iterable
from django.db import models

# Create your models here.
from django.db import models
from cliente.models import Cliente
from articulo.models import Articulo
# from vendedor.models import Vendedor
from vendedor.models import Vendedor
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation


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
        return format_html(f"\nVenta del {self.fecha_compra} al cliente {self.cliente}")
    
    def save(self,*args, **kwargs) -> None:
        super().save(*args, **kwargs)
        new_pedido = Pedido(venta=self, id=self.id)
        new_pedido.save()
    
    @property
    def precio_total(self):
        if not self.ventas.exists():
            return 0
        return sum([articulo.get_precio_total() for articulo in self.ventas.all()])

    def generar_link(self):
        return format_html("<a href='/venta/{}/'>Ver venta</a>", self.id)
    
    def crear_fila_html_desde_venta(self): 
        return format_html("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td></td></tr>",
                           self.fecha_compra, self.cliente.nombre_completo(), self.pedido.estado, self.precio_total, self.generar_link())



class ArticuloVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='ventas', on_delete=models.CASCADE)
    articulo =  models.ForeignKey(Articulo, related_name='articulos_vendidos', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    precio = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        # Update stock of the related ArticuloCompraπ
        self.articulo.stock -= self.cantidad  # Assuming a stock field in ArticuloCompra
        self.articulo.save()
        super().save(*args, **kwargs)

    def get_precio_total(self):
        if self.articulo:
            return float(self.cantidad) * float(self.precio)
        else:
            return 0.0
    @property
    def precio_minorista_2(self):
        return str(self.articulo.precio_minorista)

    @property
    def total(self):
        try:
            # Clean the precio field to ensure it only contains numeric characters and a decimal point
            cleaned_precio = self.precio.replace("'", "").replace(",", "")
            return Decimal(self.cantidad) * Decimal(cleaned_precio)
        except InvalidOperation:
            # Handle the case where conversion to Decimal fails
            return Decimal(0)
    def __str__(self):
        return f"{self.cantidad} unidades de {self.articulo} en la venta {self.venta}"
    

class Pedido(models.Model):
    PENDIENTE = 'Pendiente'
    ENTREGADO = 'Entregado'
    LISTO_PARA_RETIRAR = 'Listo para retirar'

    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (ENTREGADO, 'Entregado'),
        (LISTO_PARA_RETIRAR, 'Listo para retirar'),
    ]

    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='pedido')
    pagado = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE)


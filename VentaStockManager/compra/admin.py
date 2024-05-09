from django.contrib import admin
#from .forms import CompraAdminForm
from .models import Proveedor, Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1  # Allows adding one extra detail by default

class CompraAdmin(admin.ModelAdmin):
      
    icon_name = "shopping_cart"
    inlines = [DetalleCompraInline]
    list_display = ('fecha_compra', 'proveedor', 'cantidad_compras_realizadas', 'monto_total')

    def cantidad_compras_realizadas(self, obj):
        return obj.detallecompra_set.count()

    cantidad_compras_realizadas.short_description = 'Cantidad de compras realizadas'

    
    def monto_total(self, obj):
        total = sum(detalle.precio_unitario * detalle.cantidad for detalle in obj.detallecompra_set.all())
        return f"${total:.2f}"

    monto_total.short_description = 'total de la compra'

  
class ProvedorAdmin(admin.ModelAdmin):
      icon_name = "local_shipping"
      model = Proveedor

    


admin.site.register(Proveedor, ProvedorAdmin)

admin.site.register(Compra, CompraAdmin)


#@admin.register(Compra)
#lass CompraAdmin(admin.ModelAdmin):
  #  form = CompraAdminForm
####



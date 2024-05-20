from django.contrib import admin
from datetime  import date
from django.contrib import messages
# Register your models here.
from articulo.models import Articulo
import decimal
class ArticuloAdmin(admin.ModelAdmin):

    list_display = ('marca','codigo_interno','codigo', 'nombre', 'stock', 'vence_dentro_de_60_dias', 'total_venta_por_articulo')
    search_fields = ("nombre", 'codigo', 'codigo_interno')
    # fields = ("__all__",)
    ordering = ("vencimiento",)
    icon_name = "local_play"
    model = Articulo
    
    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.articulos_vendidos.all():
            total += articulo_venta.cantidad * float(articulo_venta.precio)
        return total
    
    def agregar_10_por_ciento_al_precio(modeladmin, request, queryset):
        for obj in queryset:
            obj.precio_minorista *= decimal.Decimal(1.1)
            obj.precio_mayorista *= decimal.Decimal(1.1)
            obj.save()
        messages.success(request, "Se actualizaron los precios al 10 porciento mas exitosamente")
    
    def vence_dentro_de_60_dias(self, obj):
        return (obj.vencimiento - date.today()).days < 60
    
    admin.site.add_action(agregar_10_por_ciento_al_precio, "Actualizacion 10")


admin.site.site_header = 'Administrador Osvaldo'
admin.site.index_title = 'Osvaldo Administrador'
admin.site.site_title = 'Osvaldo Programs'
admin.site.register(Articulo, ArticuloAdmin)

from django.contrib import admin
from datetime  import date
from django.contrib import messages
# Register your models here.
from articulo.models import Articulo
from django_q.tasks import async_task
from .task import actualizar_precios_articulos_desde_drive
import decimal

class ArticuloAdmin(admin.ModelAdmin):

    list_display = ('marca','codigo_interno','codigo', 'nombre', 'stock', 'precio_minorista', 'vence_dentro_de_60_dias', 'total_venta_por_articulo')
    search_fields = ("nombre", 'codigo', 'codigo_interno')
    # fields = ("__all__",)
    ordering = ("vencimiento",)
    icon_name = "local_play"
    model = Articulo
    actions = ['agregar_10_por_ciento_al_precio', 'agregar_5_por_ciento_al_precio', 'agregar_1_por_ciento_al_precio', 'disparar_actualizar_precio_archivo']

        
    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.articulos_vendidos.all():
            # Remove any non-numeric characters except for the decimal point
            precio = articulo_venta.precio.replace("'", "").replace(",", "")
            total += articulo_venta.cantidad * float(precio)
        return total

    def disparar_actualizar_precio_archivo(self, request, queryset):
        # Aquí se dispara la tarea
        errores = actualizar_precios_articulos_desde_drive()
        if isinstance(errores, list):
            for error in errores:
                self.message_user(request, error, level=messages.WARNING)
        else:
            self.message_user(request, errores, level=messages.SUCCESS )

    disparar_actualizar_precio_archivo.short_description = "Disparar actualizar precio xlsx"
    def agregar_10_por_ciento_al_precio(modeladmin, request, queryset):

        for obj in queryset:
            obj.precio_minorista *= decimal.Decimal(1.1)
            obj.precio_mayorista *= decimal.Decimal(1.1)
            obj.save()
        messages.success(request, "Se actualizaron los precios al 10 porciento mas exitosamente")

    def agregar_5_por_ciento_al_precio(modeladmin, request, queryset):
        for obj in queryset:
            obj.precio_minorista *= decimal.Decimal(1.05)
            obj.precio_mayorista *= decimal.Decimal(1.05)
            obj.save()
        messages.success(request, "Se actualizaron los precios al 5 porciento mas exitosamente")

    def agregar_1_por_ciento_al_precio(modeladmin, request, queryset):
        for obj in queryset:
            obj.precio_minorista *= decimal.Decimal(1.01)
            obj.precio_mayorista *= decimal.Decimal(1.01)
            obj.save()
        messages.success(request, "Se actualizaron los precios al 1 porciento mas exitosamente")
  
    def vence_dentro_de_60_dias(self, obj):
        return (obj.vencimiento - date.today()).days < 60
    
    vence_dentro_de_60_dias.boolean = True
    vence_dentro_de_60_dias.short_description = "Vence menos 60 días"
    
    
# # admin.site.get_app_list = get_app_list
# admin.site.site_header = 'Administrador Osvaldo'
# admin.site.index_title = 'Osvaldo Administrador'
# admin.site.site_title = 'Osvaldo Programs'
# admin.site.register(Articulo, ArticuloAdmin)

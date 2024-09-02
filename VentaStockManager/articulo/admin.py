from django.contrib import admin
from datetime  import date
from django.contrib import messages
# Register your models here.
from articulo.models import Articulo
from django_q.tasks import async_task
from .task import actualizar_precios_articulos_desde_drive
import decimal

class ArticuloAdmin(admin.ModelAdmin):

    list_display = ('marca','codigo_interno','codigo', 'nombre', 'stock', 'vence_dentro_de_60_dias', 'total_venta_por_articulo')
    search_fields = ("nombre", 'codigo', 'codigo_interno')
    # fields = ("__all__",)
    ordering = ("vencimiento",)
    icon_name = "local_play"
    model = Articulo
    actions = ['agregar_10_por_ciento_al_precio', 'agregar_5_por_ciento_al_precio', 'agregar_1_por_ciento_al_precio', 'disparar_actualizar_precio_archivo']

    
    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.articulos_vendidos.all():
            total += articulo_venta.cantidad * float(articulo_venta.precio)
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
    

def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    
    # Debugging: Print or log the app_dict to inspect its structure    
    # Ensure all values in app_dict are dictionaries with a 'name' key
    for app in app_dict.values():
        if not isinstance(app, dict) or 'name' not in app:
            raise ValueError(f"Invalid app entry: {app}")
    
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
    return app_list

# # admin.site.get_app_list = get_app_list
# admin.site.site_header = 'Administrador Osvaldo'
# admin.site.index_title = 'Osvaldo Administrador'
# admin.site.site_title = 'Osvaldo Programs'
# admin.site.register(Articulo, ArticuloAdmin)

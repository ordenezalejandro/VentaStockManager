# from django.contrib import admin
from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from django import forms
from django.utils import timezone
# import autocomplete_all

# from django.db.models.query import SelectQuerySet
from django.contrib import admin
from venta.forms import ArticuloVentaForm
from vendedor.models import Vendedor
class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    form = ArticuloVentaForm
    extra = 4
    verbose_name = "Item de venta"
    verbose_name_plural = "Items de ventas"
    empty_value_display = 'Busca un articulo'
    # search_fields = ('codigo', 'codigo_interno', "nombre")
    raw_id_fields = ["articulo"]
    # autocomplete_fields = ["articulo"]
    
    # prepopulated_fields  = {'precio': ('precio_minorista_2',)}
    
    # def formfield_overrides(self, request, form):
    #     overrides = super().formfield_overrides(request, form)
    #     if form.model == ArticuloVenta:
    #         overrides["articulo"] = {"widget": forms.Select(attrs={"style": "width: 200px"})}
    #     return overrides

    def precio_total(self, obj):
        if obj.cantidad is None or obj.price is None:
            return 0
        return obj.total
    readonly_fields = ("precio_total", )
    fields = ("articulo", "cantidad" , "precio", "precio_total")
    
    precio_total.short_description = "Total"
    
    # def formfield_overrides(self, request, form):
    #     overrides = super().formfield_overrides(request, form)        
    #     if form.model == ArticuloVenta:
    #         overrides["articulo"] = {"widget": forms.Select(attrs={"style": "width: 200px"})}
    #     return overrides

    # def precio_minorista_2(self, obj):
    #     if obj.articulo is None:
    #         return "-- select-articulo-first"q23
    #     return str(obj.articulo.precio_minorista)
    #readonly_fields = ('precio_minorista', 'precio_mayorista')(self, request, queryset)
    class Media:
        js = ('js/articulo_venta_admins.js',)

class VentaAdmin(admin.ModelAdmin):
    list_display = ['fecha_compra', 'fecha_entrega', 'cliente', 'vendedor', 'total_venta_por_articulo', 'vendedor']
    list_filter = ['fecha_compra', 'fecha_entrega']
    icon_name = "monetization_on"
    inlines = [ArticuloVentaInline]
    def cantidad_articulos_vendidos(self, obj):
        return obj.articulos_vendidos.count()

    cantidad_articulos_vendidos.short_description = 'Cantidad de artículos vendidos'
    
    def get_changeform_initial_data(self, request):
        # Obtiene los datos iniciales para el formulario de creación
        initial = super().get_changeform_initial_data(request)
        initial['vendedor'] = Vendedor.objects.get_or_create(usuario=request.user)
        initial['fecha_venta'] = timezone.now()
        return initial

    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.ventas.all():
            total += articulo_venta.cantidad * float(articulo_venta.precio)
        return total

    total_venta_por_articulo.short_description = 'Total Venta por Artículo'
  

    def precio_total(self, venta):
        if not venta.id:
            return f'\n{" "*8}$0.00'
        else:
            return venta.precio_total

    precio_total.short_description = 'Total De compra'
    readonly_fields = ('precio_total',)

    fieldsets = (
        ("Detalle the venta", {
            "fields":  (("cliente", "fecha_entrega", "fecha_compra"), ("precio_total", "vendedor" )),
            "classes": ('fw-bold', 'align-right', 'required'),
        }),
    )
    search_fields = ('cliente__nombre', )
    data_hierarchy = "fecha_compra"
            
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'precio_total' in form.base_fields:
            form.base_fields['precio_total'].widget.attrs['id'] = 'id_precio_total'
        return form

admin.site.register(Venta, VentaAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'pagado', 'estado']  
    list_filter = ['estado']  
    icon_name = "library_books"

admin.site.register(Pedido, PedidoAdmin)

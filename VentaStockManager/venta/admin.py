# from django.contrib import admin
from venta.models import Venta, ArticuloVenta
from articulo.models import Articulo
from django import forms

# from django.db.models.query import SelectQuerySet
import autocomplete_all as admin


class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    extra = 4
    verbose_name = "Item de venta"
    verbose_name_plural = "Items de ventas"
    
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
    #         return "-- select-articulo-first"
    #     return str(obj.articulo.precio_minorista)
    #readonly_fields = ('precio_minorista', 'precio_mayorista')(self, request, queryset)


    class Media:
        js = ('js/articulo_venta_admin.js',)

class VentaAdmin(admin.ModelAdmin):
    list_display = ['fecha_compra', 'fecha_entrega', 'cliente', 'vendedor']
    list_filter = ['fecha_compra', 'fecha_entrega']
    inlines = [ArticuloVentaInline]

    def precio_total(self, obj):
        if not obj.total:
            return 0
        else:
            obj.precio_total or 0

    precio_total.short_description = 'Total De compra'
    readonly_fields = ('precio_total',)

    fieldsets = (
        ("Detalle the venta", {
            "fields":  (("cliente", "fecha_entrega", "fecha_compra"), ("precio_total", "vendedor" )),
            "classes": ('fw-bold', 'align-right', 'required'),
        }),
    )
    # search_fields = ('cliente__nombre', )
    data_hierarchy = "fecha_compra"
admin.site.register(Venta, VentaAdmin)


# from django.contrib import admin
from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from vendedor.models import Vendedor
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django import forms
from django.utils import timezone
from .views import generar_pdf_pedidos

# import autocomplete_all

# from django.db.models.query import SelectQuerySet
from django.contrib import admin
from venta.forms import ArticuloVentaForm, VentaForm
class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    form = ArticuloVentaForm
    extra = 12
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
    form = VentaForm
    list_display = ['fecha_compra', 'fecha_entrega', 'cliente', 'vendedor', 'total_venta_por_articulo']
    list_filter = ['fecha_compra', 'fecha_entrega']
    icon_name = "monetization_on"
    inlines = [ArticuloVentaInline]
    search_fields = ('cliente__nombre')
    data_hierarchy = "fecha_compra"
    raw_id_fields = ["cliente"]
    autocomplete_fields = ['cliente']

    
    
    def cantidad_articulos_vendidos(self, obj):
        return obj.articulos_vendidos.count()

    cantidad_articulos_vendidos.short_description = 'Cantidad de artículos vendidos'
    
    def get_changeform_initial_data(self, request):
        # Obtiene los datos iniciales para el formulario de creación
        initial = super().get_changeform_initial_data(request)
        vendedor, created = Vendedor.objects.get_or_create(usuario=request.user)
        
        initial['vendedor'] = vendedor
        initial['fecha_compra'] = timezone.now()
        return initial  

    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.venta.ventas.all():  # Corrected line
            precio = articulo_venta.precio.replace("'", "").replace(",", "")
            total += articulo_venta.cantidad * float(precio)
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
        ("Detalle de venta", {
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

# admin_site.site.register(Venta, VentaAdmin)

class PedidoAdmin(admin.ModelAdmin):
    
    readonly_fields = ('venta','mostrar_articulos')
    list_display = ['id', 'venta_fecha_compra', 'venta_fecha_entrega', 'venta_cliente', 'venta_vendedor', 'total_venta_por_articulo', 'cantidad_articulos_vendidos', 'descargar_pdf']
    list_filter = ['estado', 'venta__fecha_compra', 'venta__fecha_entrega']  
    icon_name = "library_books"
    actions = ['generar_pdfs']

    # Define constants
    ARTICULO_LABEL = 'Artículo'
    
    def cantidad_articulos_vendidos(self, obj):
        return sum(articulo_venta.cantidad for articulo_venta in obj.venta.ventas.all())
    cantidad_articulos_vendidos.short_description = '# Artículos'


    def total_venta_por_articulo(self, obj):
        total = 0
        for articulo_venta in obj.articulos.all():
            precio = articulo_venta.precio.replace("'", "").replace(",", "")
            total += articulo_venta.cantidad * float(precio)
        return total


    total_venta_por_articulo.short_description = 'Total Venta'

    def venta_fecha_compra(self, obj):
        return obj.venta.fecha_compra
    venta_fecha_compra.short_description = 'Fecha de Compra'

    def venta_fecha_entrega(self, obj):
        return obj.venta.fecha_entrega
    venta_fecha_entrega.short_description = 'Fecha de Entrega'

    def venta_cliente(self, obj):
        return obj.venta.cliente
    venta_cliente.short_description = 'Cliente'

    def venta_vendedor(self, obj):
        return obj.venta.vendedor
    venta_vendedor.short_description = 'Vendedor'
    
    def descargar_pdf(self, obj):
        if obj:
            url = reverse('generar_pdf_pedido', args=[obj.id])
            return format_html('<a href="{}" target="_blank">Descargar PDF</a>', url)
        return ''

    descargar_pdf.short_description = 'Descargar PDF'
    
    def generar_pdfs(self, request, queryset):
        pedido_ids = queryset.values_list('id', flat=True)
        return HttpResponseRedirect(reverse('generar_pdf_pedidos') + f"?pedidos_ids={','.join(map(str, pedido_ids))}")
    
    generar_pdfs.short_description = "Generar PDFs para pedidos seleccionados"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generar_pdfs/', self.admin_site.admin_view(self.generar_pdfs_view), name='generar_pdf_pedidos'),
        ]
        return custom_urls + urls

    def generar_pdfs_view(self, request):
        ids = request.GET.get('ids').split(',')
        return generar_pdf_pedidos(request, ids)

    def descargar_pdf(self, obj):
        if obj:
            url = reverse('generar_pdf_pedido', args=[obj.id])
            return format_html('<a href="{}" target="_blank">Descargar PDF</a>', url)
        return ''

    def mostrar_articulos(self, obj):
        if obj.venta:
            articulosVentas = obj.venta.ventas.all()
            html = '<table>'
            html += "<tr><th>Nombre</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr>"
            for articuloVenta in articulosVentas:
                html += f"<tr><td>{articuloVenta.articulo.get_articulo_short_name()}</td>" \
                        f"<td>{articuloVenta.cantidad}</td>" \
                        f"<td>{articuloVenta.precio}</td>" \
                        f"<td>{articuloVenta.total}</td></tr>"
            html +=f"<tr><td colspan='3'><strong>Total</strong> </td><td><p style='color:blue'><b>{obj.venta.precio_total}</b></p></td></tr>"
            html += "</table>"
            html += f'<br> {self.descargar_pdf(obj)}'
            return format_html(html)
        return "No hay artículos"
    mostrar_articulos.short_description = 'Artículos de la Venta'

    fieldsets = (
        (None, {
            'fields': ('venta', 'estado',
                       ('mostrar_articulos',))
        }),
    )

    # def get_readonly_fields(self, request, obj=None):
    #        return self.readonly_fields + ('venta',)
    #     return self.readonly_fields



# admin_site.site.register(Pedido, PedidoAdmin)

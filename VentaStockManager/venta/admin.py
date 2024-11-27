# from django.contrib import admin
from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from vendedor.models import Vendedor
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils import timezone
from venta.views import generar_pdf_pedidos
from django.contrib import messages
from .forms import ArticuloVentaInlineFormSet
from venta.forms import ArticuloVentaForm
import logging
from django.core import validators
from django.core.exceptions import ValidationError

# import autocomplete_all

# from django.db.models.query import SelectQuerySet
from django.contrib import admin
from venta.forms import   VentaForm


class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    form = ArticuloVentaForm
    formset = ArticuloVentaInlineFormSet
    extra = 12
    min_num = 0
    max_num = None
    validate_min = False
    validate_max = False
    can_delete = True
    verbose_name = "Item de venta"
    verbose_name_plural = "Items de ventas"
    empty_value_display = 'Busca un articulo'
    raw_id_fields = ["articulo"]
    show_add_another = True
    show_change_link = True
    autocomplete_fields = ["articulo"]
    
    fields = ("articulo", "cantidad", "precio", "precio_total")
    readonly_fields = ("precio_total",)

    
    def precio_total(self, obj):
        if obj.cantidad is None or obj.price is None:
            return 0
        return obj.total
    readonly_fields = ("precio_total", )
    fields = ("articulo", "cantidad" , "precio", "precio_total")
    
    precio_total.short_description = "Total"
    def has_delete_permission(self, request, obj=None):
        return True
    
    def clean(self):
        cleaned_data = super().clean()
        if not self.cleaned_data.get('DELETE', False):
            cantidad = cleaned_data.get('cantidad')
            if cantidad is None or cantidad <= 0:
                raise ValidationError("La cantidad debe ser mayor que cero.")
        return cleaned_data
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "articulo":
            kwargs["queryset"] = Articulo.objects.filter(stock__gt=0)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    def save_model(self, request, obj, form, change):
        # Save the main object first to get an ID
        super().save_model(request, obj, form, change)


    
    def save_related(self, request, form, formsets, change):
        """
        Save related objects and calculate total.
        """
        try:
            total_venta = 0
            
            # Save formsets
            for formset in formsets:
                # Validate and clean formset data before saving
                if formset.is_valid():
                    instances = formset.save(commit=False)
                    
                    # Process each instance
                    for instance in instances:
                        if instance.articulo_id and instance.cantidad and instance.precio:
                            instance.venta = form.instance
                            instance.save()
                            
                            # Calculate running total
                            precio_limpio = float(str(instance.precio).replace("'", "").replace(",", ""))
                            total_venta += instance.cantidad * precio_limpio
                    
                    # Handle deletions
                    for obj in formset.deleted_objects:
                        obj.delete()
            
            # Update total sale price
            form.instance.precio_total = total_venta
            form.instance.save()
            
            messages.success(request, f'Venta actualizada. Total: ${total_venta:,.2f}')
        except Exception as e:
            logging.error(f"Error in save_related: {str(e)}")
            messages.error(request, f"Error al guardar la venta: {str(e)}")
            raise
    
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
        for articulo_venta in obj.ventas.all():
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

    def save_formset(self, request, form, formset, change):
        try:
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.articulo and instance.cantidad and instance.precio:
                    instance.venta = form.instance
                    instance.save()
            
            # Handle deletions
            for obj in formset.deleted_objects:
                obj.delete()
            
        except Exception as e:
            messages.error(request, str(e))
            raise

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
        for articulo_venta in obj.venta.ventas.all():
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

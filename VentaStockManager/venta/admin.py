from django.contrib import admin
from venta.models import Venta, ArticuloVenta

class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    extra = 1
    readonly_fields = ('precio_minorista', 'precio_mayorista')
    
    def get_formset(self, request, obj=None, **kwargs):        # First get the base formset class
        BaseFormSet = kwargs.pop("formset", self.formset)
 
        # Now make a custom subclass with an overridden “get_form_kwargs()”
        class CustomFormSet(BaseFormSet):
            def get_form_kwargs(self, index):
                kwargs = super().get_form_kwargs(index)                # kwargs["parent_obj"] = obj
                return kwargs
 
        # Finally, pass our custom subclass to the superclass’s method. This
        # will override the default.
        kwargs["formset"] = CustomFormSet
        return super().get_formset(request, obj, **kwargs)


class VentaAdmin(admin.ModelAdmin):
    inlines = [ArticuloVentaInline]
    list_display = ['fecha_compra', 'fecha_entrega', 'cliente']
    list_filter = ['fecha_compra', 'fecha_entrega']
    search_fields = ['cliente__nombre', 'cliente__apellido']
        
admin.site.register(Venta, VentaAdmin)


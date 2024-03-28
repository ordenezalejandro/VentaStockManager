from django.contrib import admin
from venta.models import Venta, ArticuloVenta
from articulo.models import Articulo
# from django.db.models.query import SelectQuerySet


class ArticuloVentaInline(admin.TabularInline):
    model = ArticuloVenta
    extra = 1
    search_fields = ('codigo', 'codigo_interno', "nombre")
    autocomplete_fields = ["articulo"]
    #readonly_fields = ('precio_minorista', 'precio_mayorista')

    
    def get_formset(self, request, obj=None, **kwargs):        # First get the base formset class
        BaseFormSet = kwargs.pop("formset", self.formset)
 
        # Now make a custom subclass with an overridden “get_form_kwargs()”
        # class CustomArticuloQueryset(SelectQuerySet):
        #     def __init__(self, model, renderer, can_filter=True, use_distinct=False, db=None, *, where=None, params=None, ordered=False, lo_limit=5, hi_limit=None):
        #         super().__init__(model, renderer, can_filter, use_distinct, db, where=where, params=params, ordered=ordered, lo_limit=lo_limit, hi_limit=hi_limit)
        #         if request is not None:
        #             search_term = request.GET.get('q', '')
        #             if search_term:
        #                 where = self.where or []
        #                 where.append(models.Q(codigo_interno__icontains=search_term) | models.Q(codigo__icontains=search_term) | models.Q(nombre__icontains=search_term))
        #                 self._where = where

        class CustomFormSet(BaseFormSet):
            def get_form_kwargs(self, index):
                kwargs = super().get_form_kwargs(index)                # kwargs["parent_obj"] = obj
                return kwargs
 
        # Finally, pass our custom subclass to the superclass’s method. This
        # will override the default.
        
        # kwargs['queryset'] = CustomArticuloQueryset(Articulo, None)
        kwargs["formset"] = CustomFormSet
        return super().get_formset(request, obj, **kwargs)


class VentaAdmin(admin.ModelAdmin):
    inlines = [ArticuloVentaInline]
    list_display = ['fecha_compra', 'fecha_entrega', 'cliente']
    list_filter = ['fecha_compra', 'fecha_entrega']

admin.site.register(Venta, VentaAdmin)


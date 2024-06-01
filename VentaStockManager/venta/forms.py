from dal import autocomplete
from django import forms

from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse
from venta.models import ArticuloVenta
from .models import Pedido, Venta
from  cliente.models import Cliente
from django.urls import reverse
from django_addanother.widgets import AddAnotherWidgetWrapper


from django import forms
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete',
                        attrs={'data-placeholder': 'Buscar Articulo', 'empty_label': 'No_seleccionado'})
,
        }
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget = RelatedFieldWidgetWrapper(
            self.fields['cliente'].widget,
            Venta._meta.get_field('cliente').remote_field,
            admin.site,
            can_add_related=True,
            can_change_related=True,
            can_delete_related=False
        )   
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'cliente' in self.fields:
    #         cliente_field = self.fields['cliente']
    #         cliente_field.widget = forms.widgets.Select(attrs={'style': 'width: 80%;'})
    #         cliente_field.widget.can_add_related = True
    #         cliente_field.widget.attrs['data-add-object-url'] = reverse('admin:cliente_cliente_add')

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js',
            'js/init_select2.js',
        )
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css',),
        }

class ArticuloVentaForm(forms.ModelForm):
    class Meta:
        model = ArticuloVenta
        fields = ('__all__')
        widgets = {
            'articulo': autocomplete.ModelSelect2(url='articulo-autocomplete',
                        attrs={'data-placeholder': 'Buscar Articulo', 'empty_label': 'No_seleccionado'})
        }

class PedidoEstadoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['pagado', 'estado']
        labels = {
            'pagado': 'Pagado',
            'estado': 'Estado',
        }
        widgets = {
            'pagado': forms.CheckboxInput(),
            'estado': forms.Select(choices=Pedido.ESTADO_CHOICES),
        }

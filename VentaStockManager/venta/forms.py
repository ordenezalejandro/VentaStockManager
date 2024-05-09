from dal import autocomplete

from django import forms
from venta.models import ArticuloVenta
from .models import Pedido


class ArticuloVentaForm(forms.ModelForm):
    class Meta:
        model = ArticuloVenta
        fields = ('__all__')
        widgets = {
            'articulo': autocomplete.ModelSelect2(url='articulo-autocomplete')
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

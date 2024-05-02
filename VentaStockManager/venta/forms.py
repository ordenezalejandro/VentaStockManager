from dal import autocomplete

from django import forms
from venta.models import ArticuloVenta

class ArticuloVentaForm(forms.ModelForm):
    class Meta:
        model = ArticuloVenta
        fields = ('__all__')
        widgets = {
            'articulo': autocomplete.ModelSelect2(url='articulo-autocomplete')
        }

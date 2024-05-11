from dal import autocomplete

from django import forms
from venta.models import ArticuloVenta

class ArticuloVentaForm(forms.ModelForm):
    class Meta:
        model = ArticuloVenta
        fields = ('__all__')
        widgets = {
            'articulo': autocomplete.ModelSelect2(url='articulo-autocomplete',
                        attrs={'data-placeholder': 'Buscar Articulo', 'empty_label': 'No_seleccionado'})
        }
    def __init__(self, *args, **kwargs):
            super(ArticuloVentaForm, self).__init__(*args, **kwargs)
            self.fields['articulo'].widget.attrs['initial'] = 'No_seleccionado'
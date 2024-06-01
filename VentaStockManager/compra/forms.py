from dal import autocomplete
from django import forms
from .models import Compra, Proveedor

class CompraAdminForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=autocomplete.ModelSelect2(url='proveedor-autocomplete')
    )
    class Meta:
        model = Compra
        fields = '__all__'

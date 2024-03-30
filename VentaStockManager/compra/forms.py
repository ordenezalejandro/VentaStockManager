from django import forms
from .models import Compra

class CompraAdminForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)

    class Meta:
        model = Compra
        fields = '__all__'

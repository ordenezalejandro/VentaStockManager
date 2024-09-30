from dal import autocomplete
from django import forms

from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.urls import reverse
from venta.models import ArticuloVenta
from .models import Pedido, Venta
from  cliente.models import Cliente
from django.urls import reverse
from django.forms.models import BaseInlineFormSet

# from django_addanother.widgets import AddAnotherWidgetWrapper


from django import forms
import logging

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete',
                        attrs={'data-placeholder': 'Buscar Cliente', 'empty_label': 'No_seleccionado'})
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

class ArticuloVentaInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                continue  # Skip validation for forms marked for deletion

    @property
    def media(self):
        logging.debug("Constructing media for ArticuloVentaInlineFormSet")
        media = super().media
        logging.debug(f"Media: {media}")
        return media

    def _construct_form(self, i, **kwargs):
        logging.debug(f"Constructing form {i} with kwargs: {kwargs}")
        form = super()._construct_form(i, **kwargs)
        logging.debug(f"Constructed form {i}: {form}")
        return form

class ArticuloVentaForm(forms.ModelForm):
    class Meta:
        model = ArticuloVenta
        fields = '__all__'
        widgets = {
            'articulo': autocomplete.ModelSelect2(url='articulo-autocomplete',
                        attrs={'data-placeholder': 'Buscar Articulo', 'empty_label': 'No seleccionado'})
        }

    def __init__(self, *args, **kwargs):
        super(ArticuloVentaForm, self).__init__(*args, **kwargs)
        if 'articulo' in self.fields:
            self.fields['articulo'].widget = RelatedFieldWidgetWrapper(
                self.fields['articulo'].widget,
                ArticuloVenta._meta.get_field('articulo').remote_field,
                admin.site,
                can_add_related=True,
                can_change_related=False,
                can_delete_related=False
            )
        logging.debug(f"Initialized ArticuloVentaForm with fields: {self.fields}")

    def clean(self):
        if self.data.get(f'{self.prefix}-DELETE', 'off') == 'on'or self.data.get('id') is None:
            logging.info(f"Skipping validation for {self.prefix} as it is marked for deletion.")
            # Set required fields to False to skip validation
            self.fields['articulo'].required = False
            self.fields['cantidad'].required = False
            self.fields['precio'].required = False
            return self.cleaned_data  # Skip further validation if marked for deletion
        
        cleaned_data = super().clean()
        logging.debug(f"Cleaned data: {cleaned_data}")
        # Add your custom validation logic here if needed
        return cleaned_data

    def is_valid(self):
        if self.data.get(f'{self.prefix}-DELETE', 'off') == 'on' or self.data.get('id') is None:
            logging.info(f"Form {self.prefix} is marked for deletion, skipping validation.")
            valid = super().is_valid()
            return True  # Consider the form valid if marked for deletion
        valid = super().is_valid()
        if not valid:
            logging.error(f"Form errors for {self.prefix}: {self.errors}")
        else:
            logging.debug(f"Form valid for {self.prefix}: {valid}")
        return valid

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

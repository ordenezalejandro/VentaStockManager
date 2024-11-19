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
        from VentaStockManager.admin import admin_site  # Local import

        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget = RelatedFieldWidgetWrapper(
            self.fields['cliente'].widget,
            Venta._meta.get_field('cliente').remote_field,
            admin_site=admin_site,
            can_add_related=True,
            can_change_related=True,
            can_delete_related=True
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._deleted_objects = []

    def clean(self):
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            # Skip validation for forms marked for deletion
            if form.cleaned_data.get('DELETE', False) or form.cleaned_data == {}:
                logging.info(f"Skipping validation for form {form.prefix} as it is marked for deletion.")
                continue

            # Add any additional validation logic here if needed
            if not form.cleaned_data.get('articulo'):
                form.add_error('articulo', 'This field is required.')
            if not form.cleaned_data.get('cantidad'):
                form.add_error('cantidad', 'This field is required.')
            if not form.cleaned_data.get('precio'):
                form.add_error('precio', 'This field is required.')
        return super().clean()

    @property
    def deleted_objects(self):
        return self._deleted_objects

    @deleted_objects.setter
    def deleted_objects(self, value):
        self._deleted_objects = value

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
        from VentaStockManager.admin import admin_site  # Local import
        if 'articulo' in self.fields:
            self.fields['articulo'].widget = RelatedFieldWidgetWrapper(
                self.fields['articulo'].widget,
                ArticuloVenta._meta.get_field('articulo').remote_field,
                admin_site=admin_site,
                can_add_related=True,
                can_change_related=True,
                can_delete_related=True
            )
        logging.debug(f"Initialized ArticuloVentaForm with fields: {self.fields}")

    def clean(self):
        cleaned_data = super().clean()
        logging.debug(f"Data received for cleaning: {self.data}")
        # Check if the form is marked for deletion
        if self.fields['DELETE'] or self.cleaned_data == {}:
            logging.info(f"Skipping validation for {self.prefix} as it is marked for deletion.")
            # Set required fields to False to skip validation
            self.fields['articulo'].required = False
            self.fields['cantidad'].required = False
            self.fields['precio'].required = False
            return self.cleaned_data
        
        # Ensure all required fields are present
        if not cleaned_data.get('articulo'):
            self.add_error('articulo', 'This field is required.')
        if not cleaned_data.get('cantidad'):
            self.add_error('cantidad', 'This field is required.')
        if not cleaned_data.get('precio'):
            self.add_error('precio', 'This field is required.')

        return cleaned_data

    def is_valid(self):
        # Check if the form is marked for deletion
        if self.data.get('DELETE') or self.cleaned_data == {}:
            logging.info(f"Form {self.prefix} is marked for deletion, skipping validation.")
            return True
        valid = super().is_valid()
        if not valid:
            logging.error(f"Form errors for {self.prefix}: {self.errors}")
        else:
            logging.debug(f"Form valid for {self.prefix}: {valid}")
        return valid

    def save(self, commit=True):
        # Skip saving if marked for deletion
        if self.cleaned_data.get('DELETE', False) or self.cleaned_data == {}:
            logging.info(f"Skipping save for {self.prefix} as it is marked for deletion.")
            return None
        if self.is_valid():
            instance = super().save(commit=False)
            if commit:
                instance.save()
            return instance
        else:
            logging.error(f"Cannot save form {self.prefix} due to errors: {self.errors}")
            return None
    
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

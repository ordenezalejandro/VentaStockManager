from django.urls import path
from .views import formulario_compra, ProveedorAutocomplete

urlpatterns = [
    path('cargar_compra_por_imagen/', formulario_compra, name='cargar_compra'),
    path('proveedor-autocomplete/', ProveedorAutocomplete.as_view(), name='proveedor-autocomplete'),

    # Otros patrones de URL de tu aplicación
]

from django.urls import path
from .views import formulario_compra

urlpatterns = [
    path('cargar_compra_por_imagen/', formulario_compra, name='cargar_compra'),
    # Otros patrones de URL de tu aplicación
]

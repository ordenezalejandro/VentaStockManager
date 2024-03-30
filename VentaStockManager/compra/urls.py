from django.urls import path
from .views import formulario_compra

urlpatterns = [
    path('formulario/', formulario_compra, name='formulario_compra'),
    # Otros patrones de URL de tu aplicación
]

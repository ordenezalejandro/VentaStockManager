from django.urls import path
from .views import mostrar_articulos

urlpatterns = [
    path('mostrar_articulos/', mostrar_articulos, name='mostrar_articulos'),
    # Otros patrones de URL de tu aplicación
]

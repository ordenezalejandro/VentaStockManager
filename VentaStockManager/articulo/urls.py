from django.urls import path
from .views import mostrar_articulos, lista_precios

urlpatterns = [
    path('mostrar_articulos/', mostrar_articulos, name='mostrar_articulos'),
    path('lista_precios/', lista_precios, name='lista_precio'),    # Otros patrones de URL de tu aplicación
]

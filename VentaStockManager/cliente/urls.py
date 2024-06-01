from django.urls import path
from .views import (
    mostrar_todos_los_clientes,
    procesar_nuevo_cliente,
    ListaArticulosView,
    ClienteAutocomplete
    
    )
# from . import views (
#     mis_articulos,
#     )  # Importa las vistas de tu aplicación
    
urlpatterns = [
    # path('mayor_de_edad/', filtrar_por_mayor_de_edad, name='filtrar_por_mayor_de_edad'),
    # path('menor_de_edad/', filtrar_por_menor_de_edad, name='filtrar_por_menor_de_edad'), 
    # path('de_18/', filtrar_por_de_18, name='filtrar_por_de_18'),
    path('mostrar_todos_los_clientes/', mostrar_todos_los_clientes, name='clientes'), 
    path('procesar_nuevo_cliente/', procesar_nuevo_cliente, name='procesar_cliente'), 
    path('mis-articulos/', ListaArticulosView.as_view(), name='mis_articulos'),
    path('cliente-autocomplete/', ClienteAutocomplete.as_view(), name='cliente-autocomplete')
    # Define la URL '/mis-articulos/' y asigna la vista ListaArticulosView
]

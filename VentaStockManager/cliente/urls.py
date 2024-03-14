from django.urls import path
from .views import (
    filtrar_por_mayor_de_edad,
    filtrar_por_menor_de_edad,
    filtrar_por_de_18,mostrar_todos_los_clientes,
    procesar_nuevo_cliente
    )


urlpatterns = [
    path('mayor_de_edad/', filtrar_por_mayor_de_edad, name='filtrar_por_mayor_de_edad'),
    path('menor_de_edad/', filtrar_por_menor_de_edad, name='filtrar_por_menor_de_edad'), 
    path('de_18/', filtrar_por_de_18, name='filtrar_por_de_18'),
    path('mostrar_todos_los_clientes/', mostrar_todos_los_clientes, name='clientes'), 
    path('procesar_nuevo_cliente/', procesar_nuevo_cliente, name='procesar_cliente'), 
]
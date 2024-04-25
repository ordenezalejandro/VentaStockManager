from django.urls import path
from .views import mostrar_todos_los_vendedores, procesar_nuevo_vendedor


urlpatterns = [
    path('mostrar_todos_los_vendedoress/', mostrar_todos_los_vendedores, name='vendedores'), 
    path('procesar_nuevo_cliente/', procesar_nuevo_vendedor, name='procesar_vendedor'), 
]
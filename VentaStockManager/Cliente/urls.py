from django.urls import path
from .views import filtrar_por_mayor_de_edad

urlpatterns = [
    path('mayor_de_edad/', filtrar_por_mayor_de_edad, name='filtrar_por_mayor_de_edad'),
]
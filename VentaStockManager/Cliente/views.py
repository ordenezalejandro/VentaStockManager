from django.shortcuts import render
from Cliente.models import Cliente
from django.http import HttpResponse


# Create your views here.
def filtrar_por_mayor_de_edad(request):
    clientes_mayores = Cliente.objects.filter(edad__gte=18) 
    return HttpResponse(f"Clientes mayores de edad: {''.join(['<p>' + str(cliente) + '</p>' for cliente in clientes_mayores])}")
from django.shortcuts import render
from Cliente.models import Cliente
from django.http import HttpResponse


#Cliente/cliente/ Create your views here.
def filtrar_por_mayor_de_edad(request):
    clientes_mayores = Cliente.objects.filter(edad__gte=18) 
    return HttpResponse(f"Clientes mayores de edad: {''.join(['<p>' + str(cliente) + '</p>' for cliente in clientes_mayores])}")

# Create your views here.
def filtrar_por_menor_de_edad(request):# Create your views here.
    clientes_menores = Cliente.objects.filter(edad__lte=18) 
    return render(request, 'clientes.html', {'clientes': clientes_menores})

def filtrar_por_de_18 (request):# Create your views here.
    clientes_de_18 = Cliente.objects.filter(edad=18) 
    return render(request, 'clientes.html', {'clientes': clientes_de_18})
    
def mostrar_todos_los_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})



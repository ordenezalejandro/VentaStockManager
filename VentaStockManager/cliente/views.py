from django.shortcuts import render
from cliente.models import Cliente
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView
from articulo.models import Articulo
from dal import autocomplete
from django.db import models
from dal import autocomplete



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


def procesar_nuevo_cliente(request):
    # process
    if request.method == 'POST':
        # saco los datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        contrasena = request.POST.get('contrasena')
        cuil = request.POST.get('cuil')
        telefono = request.POST.get('telefono')
        edad = request.POST.get('edad')
        genero = request.POST.get('genero') 
        email = request.POST.get('email')
        # creo el usuario     
        perfil = User(email=email, password=contrasena, username=email)
        perfil.save()
        new_cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            cuil=cuil,
            telefono=telefono,
            sexo=genero,
            perfil=perfil,
            edad=edad
        )
        try:
            new_cliente.save()
        except ValidationError as e:
            return HttpResponse('error en validadtion de dato.')

    else:
        return render(request, 'formulario_cliente.html')
    
class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cliente.objects.none()
        if self.q:
            clientes = Cliente.objects.filter(
                models.Q(nombre__icontains=self.q)|
                models.Q(codigo_interno__icontains=self.q) |
                models.Q(apellido__icontains=self.q))
        else:   
            clientes = Cliente.objects.all()
        return clientes
        
# # En tus vistas
# if request.user.has_perm('cliente.puede_acceder_lista_articulos'):
#     # Realiza alguna acción si el usuario tiene el permiso

class ListaArticulosView(ListView):
    model = Articulo
    template_name = 'lista_articulos.html'

 
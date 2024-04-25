from django.shortcuts import render
from vendedor.models import Vendedor
from django.contrib.auth.decorators import login_required


# Create your views here.

def mostrar_todos_los_vendedores(request):
    vendedores = vendedor.objects.all()
    return render(request, 'vendedores.html', {'vendedores': vendedores})


def procesar_nuevo_vendedor(request):
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
        # creo el vendedor     perfil = User(email=email, password=contrasena, username=email)
        new_vendedor = Vendedor(
            email=email,
            nombre=nombre,
            apellido=apellido,
            cuil=cuil,
            telefono=telefono,
            sexo=genero,
            edad=edad
        )
        try:
            new_vendedor.save()
        except ValidationError as e:
            return HttpResponse('error en validadtion de dato.')

    else:
        return render(request, 'formulario_cliente.html')

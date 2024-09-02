from django.shortcuts import render, HttpResponse
from .models import Articulo
from django.contrib import messages
import decimal


def mostrar_articulos(request):
    # Recupera todos los artículos del modelo Articulo
    if request.method == 'POST':
        articulos_ids = request.POST.getlist("articulo-ids")
      
        articulos_seleccionados = Articulo.objects.filter(id__in=articulos_ids)
        try:
            porcentage_desde_el_form =  int(request.POST['porcentage'])  or 0 
        except ValueError:# obtener el porcentage que vine del form. ayuda request.POST......
            errors = True       
            return render(request, 'mostrar_articulos.html', {'articulos': articulos_seleccionados   , 'errors': errors})

        for articulo in articulos_seleccionados:
            articulo.precio_venta *= decimal.Decimal(1+(0.01*porcentage_desde_el_form)) # recoradr que si queremos aumentar un 50% es igual al valor del producto multiplicado por 1.5. si queremos aumentar en 20% es igual a multiplicar a 1.2
            articulo.save()
            messages.success(request, f"articulo seleccionado {articulo}")
        return render(request, 'precio_actualizado.html', {'articulos': articulos_seleccionados})
    else:
        articulos = Articulo.objects.all()
        # Renderiza la plantilla 'mostrar_articulos.html' y pasa los artículos recuperados como contexto
        return render(request, 'mostrar_articulos.html', {'articulos': articulos})







def lista_precios(request):
    query = request.GET.get('q', '')
    if query:
        articulos = Articulo.objects.filter(nombre__icontains=query)
    else:
        articulos = Articulo.objects.all()
    
    return render(request, 'lista_precios.html', {'articulos': articulos, 'query': query})

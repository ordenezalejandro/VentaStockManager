from django.shortcuts import render
from venta.models import Venta, ArticuloVenta
from articulo.models import Articulo
from vendedor.models import Vendedor
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.db import models



class ArticuloAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:  
            return Articulo.objects.none()
        if self.q:
            articulos = Articulo.objects.filter(
                models.Q(nombre__icontains=self.q) |
                models.Q(codigo__icontains=self.q) |
                models.Q(codigo_interno__icontains=self.q)
            )
        else:
            articulos = Articulo.objects.all()
        return articulos

# Create your views here.
def venta_detalle(request, venta_id):
    """ esta vista toma in venta_id, busca la base de datos  y rendariza el template de la venta
    
    """
    # buscamos la venta por el id
    venta = Venta.objects.get(id=venta_id)
    context = {'venta': venta, 'titulo_de_pagina' : 'detalle de venta'}

    # rendarizamo el temaplate
    return render(request, 'venta_detalle.html', context)

def ventas_por_vendedor(request, id_vendedor):
    # Recupera el vendedor por su ID
    vendedor = Vendedor.objects.get(pk=id_vendedor)
    
    # Recupera las ventas asociadas al vendedor
    ventas = Venta.objects.filter(vendedor=vendedor)
    
    # Puedes hacer más procesamiento aquí si es necesario
    
    # Renderiza el template con el contexto de las ventas por vendedor
    return render(request, 'ventas_por_vendedor.html', {'vendedor': vendedor, 'ventas': ventas})


@login_required
def calcular_ganancia_articulos(request):
    # Obtener todos los artículos
    articulos = Articulo.objects.all()

    # Crear un diccionario para almacenar la ganancia de cada artículo
    ganancia_por_articulo = {}

    # Iterar sobre cada artículo
    for articulo in articulos:
        # Obtener la información de compra del artículo
        precio_compra = articulo.precio_compra

        # Obtener todas las ventas de este artículo
        ventas = ArticuloVenta.objects.filter(articulo=articulo)

        # Calcular la ganancia total por este artículo
        ganancia_total = sum(venta.articulo.precio_venta - precio_compra for venta in ventas)

        # Guardar la ganancia total en el diccionario
        ganancia_por_articulo[articulo.nombre] = ganancia_total

    # Pasar el diccionario de ganancias a la plantilla
    context = {'ganancia_por_articulo': ganancia_por_articulo}
    return render(request, 'ganancia_por_articulos.html', context)

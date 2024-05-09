from django.shortcuts import render, redirect
from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from vendedor.models import Vendedor
from .forms import PedidoEstadoForm
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



def comprovante_de_venta(request, venta_id):
    venta = Venta.objects.get(id=venta_id)
    cliente = venta.cliente  # Ajusta este campo según la estructura real de tu modelo Venta
    vendedor = venta.vendedor.fullname()# Ajusta este campo según la estructura real de tu modelo Venta
    articulos_venta = ArticuloVenta.objects.filter(venta=venta)  # Filtrar los artículos vendidos asociados a esta venta

    return render(request, 'comprovante_de_venta.html', {'venta': venta, 'cliente': cliente, 'vendedor': vendedor, 'articulos_venta': articulos_venta})


def ver_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    cliente = pedido.venta.cliente  # Ajusta este campo según la estructura real de tu modelo Venta
    vendedor = pedido.venta.vendedor.fullname()# Ajusta este campo según la estructura real de tu modelo Venta
    articulos_venta =  pedido.venta.articulos_vendidos.all()  # Filtrar los artículos vendidos asociados a esta venta
    if request.method == 'POST':
        form = PedidoEstadoForm(request.POST)
        if form.is_valid():
            pedido.pagado =  form.cleaned_data['pagado']
            pedido.estado = form.cleaned_data['estado']
            pedido.save()
              
            return redirect('admin:venta_pedido_changelist')
    
    return render(request, 'ver_pedido.html', {
        'venta': pedido.venta,
        'cliente': cliente, 
        'vendedor': vendedor, 
        'articulos_venta': articulos_venta,
        'pedido': pedido,
        'form': PedidoEstadoForm(initial={"estado": pedido.estado, 'pagado':pedido.pagado})})

      
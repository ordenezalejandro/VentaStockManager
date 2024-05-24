from django.shortcuts import render, redirect
from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from vendedor.models import Vendedor
from .forms import PedidoEstadoForm
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.db import models

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
from django.utils import timezone
from datetime import timedelta

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
    
    # def get_result_label(self, item):
    #     # Define cómo se mostrará cada opción en el menú desplegable
    #     return f"{item.articulo}"
    
    # def create_option(self, term, valor, articulo):
    #     # Crea una opción personalizada para el término especificado
    #     return {
    #         'id': valor,
    #         'text': term,
    #         'nombre': articulo.nombre,
    #         'codigo': articulo.codigo,
    #         'precio_mayorista': articulo.precio_mayorista,
    #         'precio_minorista': articulo.precio_minorista,
    #     }
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
    total_ventas = sum(venta.total for venta in ventas)

    
    # Puedes hacer más procesamiento aquí si es necesario
    context = {
        'vendedor': vendedor,
        'ventas': ventas,
        'total_ventas': total_ventas,
        'titulo_de_pagina': 'Ventas'
    }
    return render(request, 'ventas_por_vendedor.html', context)




@login_required
def ventas_recientes_por_vendedor(request, id_vendedor):
    # Recupera el vendedor por su ID
    vendedor = Vendedor.objects.get(pk=id_vendedor)
    
    # Establece la fecha de hace 7 días
    fecha_inicio = timezone.now() - timedelta(days=7)
    
    # Recupera las ventas asociadas al vendedor en los últimos 7 días
    ventas_recientes = Venta.objects.filter(vendedor=vendedor, fecha_compra__gte=fecha_inicio)
    
    # Calcula el total de ventas
    total_ventas = sum(venta.total for venta in ventas_recientes)
    
    # Renderiza el template con el contexto de las ventas recientes por vendedor
    context = {
        'vendedor': vendedor,
        'ventas': ventas_recientes,
        'total_ventas': total_ventas,
        'titulo_de_pagina': 'Ventas Recientes por Vendedor'
    }
    return render(request, 'ventas_por_vendedor.html', context)

def ventas_mensual_por_vendedor(request, id_vendedor):
    # Recupera el vendedor por su ID
    vendedor = Vendedor.objects.get(pk=id_vendedor)
    
    # Establece la fecha de hace 7 días
    fecha_inicio = timezone.now() - timedelta(days=30)
    
    # Recupera las ventas asociadas al vendedor en los últimos 7 días
    ventas_mensual = Venta.objects.filter(vendedor=vendedor, fecha_compra__gte=fecha_inicio)
    
    # Calcula el total de ventas
    total_ventas = sum(venta.total for venta in ventas_mensual)
    
    # Renderiza el template con el contexto de las ventas recientes por vendedor
    context = {
        'vendedor': vendedor,
        'ventas': ventas_mensual,
        'total_ventas': total_ventas,
        'titulo_de_pagina': 'Ventas Mensual por Vendedor'
    }
    return render(request, 'ventas_por_vendedor.html', context)
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

      
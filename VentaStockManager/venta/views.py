from django.shortcuts import render, redirect
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from venta.models import Venta, ArticuloVenta, Pedido
from articulo.models import Articulo
from vendedor.models import Vendedor
from .forms import PedidoEstadoForm
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.db import models
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak, Paragraph, Frame, PageTemplate

from io import BytesIO
from reportlab.lib import colors
from django.urls import reverse_lazy



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
    vendedor = get_object_or_404(Vendedor, pk=id_vendedor)
    
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
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame, Spacer, PageBreak
from io import BytesIO
from django.http import HttpResponse

def generar_pdf_pedidos_(request, pedido_ids=None):
    if not pedido_ids:
        pedido_ids = request.GET.getlist('ids')
    pedidos = Pedido.objects.filter(id__in=pedido_ids[0].split(","))

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    frame_width = (A4[0] - 30 * mm) / 2  # Adjusted for margin
    frame_height = (A4[1] - 30 * mm) / 2  # Adjusted for margin
    frames = [] 
    padding = 1 * mm  # Padding entre tablas

    # Define frames
    for i in range(2):
        for j in range(2):
            frames.append(Frame(
                10 * mm + i * frame_width,
                A4[1] - 10 * mm - (j + 1) * frame_height,
                frame_width - 10 * mm,
                frame_height - 10 * mm,
                id=f'frame_{i}_{j}'
            ))

    # Add page template
    pdf.addPageTemplates([PageTemplate(id='FourFrames', frames=frames)])

    quarter_count = 0

    for pedido in pedidos:
        # Información del cliente y vendedor
        data_cliente = [
            [f'Id: # {pedido.venta.id}', f'Nombre del Cliente: {pedido.venta.cliente.nombre}', '', ''],
            [f'Teléfono: ({pedido.venta.cliente.telefono})', f'Vendedor: {pedido.venta.vendedor}', '', ''],
            [f"Dirección: {pedido.venta.cliente.direccion}", f"Fecha de Compra: {pedido.venta.fecha_compra.strftime('%Y-%m-%d')}", '', '']
        ]
        data_articulos = [['Artículo', '#', 'Precio', 'Subtotal']]
        
        for articulo_venta in pedido.venta.ventas.all():
            articulo_nombre = articulo_venta.articulo.get_articulo_short_name()
            if len(articulo_nombre) > 20:  # Truncar nombres largos
                articulo_nombre = articulo_nombre[:17] + '...'
            data_articulos.append([
                articulo_nombre,
                articulo_venta.cantidad,
                articulo_venta.precio,
                articulo_venta.total
            ])
        
        # Completar las filas si hay menos de 12 artículos
        while len(data_articulos) < 13:
            data_articulos.append(['', '', '', ''])

        # Tabla del cliente
        tabla_cliente = Table(data_cliente, colWidths=[frame_width/4]*4)
        estilo_tabla_cliente = TableStyle([
            ('SPAN', (0, 0), (1, 0)),  # Combina las dos primeras celdas en la primera fila
            ('SPAN', (0, 1), (1, 1)),  # Combina las dos primeras celdas en la segunda fila
            ('SPAN', (0, 2), (1, 2)),  # Combina las dos primeras celdas en la tercera fila
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        tabla_cliente.setStyle(estilo_tabla_cliente)

        # Tabla de artículos
        tabla_articulos = Table(data_articulos, colWidths=[frame_width/4]*4)
        estilo_tabla_articulos = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ])
        tabla_articulos.setStyle(estilo_tabla_articulos)

        # Tabla del total
        data_total = [['Total:', '', '', pedido.venta.precio_total]]
        tabla_total = Table(data_total, colWidths=[frame_width/4]*4)
        estilo_tabla_total = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
        ])
        tabla_total.setStyle(estilo_tabla_total)

        # Añadir tablas a los elementos
        elements.append(tabla_cliente)
        elements.append(tabla_articulos)
        elements.append(tabla_total)
        elements.append(Spacer(1, padding))  # Agregar padding entre tablas
        
        quarter_count += 1
        
        if quarter_count % 4 == 0:
            elements.append(PageBreak())
            quarter_count = 0

    pdf.build(elements)

    pdf_buffer = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    return response

def generar_pdf_pedidos(request, pedido_ids=None):
    from reportlab.lib.pagesizes import landscape
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO
    from django.http import HttpResponse
    from .models import Pedido
    if pedido_ids is None:
        pedido_ids = request.GET.get('pedidos_ids').split(',')
        
    
    buffer = BytesIO()
    elements = []
    styles = getSampleStyleSheet()
    padding = 0.5 * cm
    pedidos_count = len(pedido_ids)
    cantidad_articulos = []
    for index, pedido_id in enumerate(pedido_ids):
        pedido = Pedido.objects.get(id=pedido_id)
        cantidad_articulos.append(pedido.venta.ventas.count())
        data_cliente = [
            ['Compra:', pedido.venta.fecha_compra, 'Entrega:', pedido.venta.fecha_entrega],
            ['Cliente:', pedido.venta.cliente.nombre_completo(), 'Dirección:', pedido.venta.cliente.direccion],
        ]

        # Tabla del cliente
        tabla_cliente = Table(data_cliente, colWidths=[2 * cm, 2 * cm, 2 * cm,  2 * cm])
        estilo_tabla_cliente = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 7)
        ])
        tabla_cliente.setStyle(estilo_tabla_cliente)

        # Tabla de artículos
        data_articulos = [['Articulos', 'Cant', 'Precio/U', 'Total']]
        for articulo_venta in pedido.venta.ventas.all():
            nombre_articulo = articulo_venta.articulo.get_articulo_short_name()
            nombre_articulo_corto = ""
            nombre_articulo_len = len(nombre_articulo)
            for i in range(0, nombre_articulo_len, 26):
                if i%26 > 0:
                    nombre_articulo_corto += nombre_articulo[i:i+26] + "\n"
                else:
                    nombre_articulo_corto += nombre_articulo[i:i+26] 
                
            data_articulos.append([
                nombre_articulo_corto,
                articulo_venta.cantidad,
                articulo_venta.precio,
                articulo_venta.total
            ])

        tabla_articulos = Table(data_articulos, colWidths=[4 * cm, 1 * cm, 1.5 * cm, 1.5 * cm])
        estilo_tabla_articulos = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7)
        ])
        tabla_articulos.setStyle(estilo_tabla_articulos)

        # Tabla del total
        data_total = [['Total:', pedido.venta.precio_total]]
        tabla_total = Table(data_total, colWidths=[5 * cm, 3 * cm])
        estilo_tabla_total = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            # ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ])
        tabla_total.setStyle(estilo_tabla_total)

        # Añadir tablas a los elementos
        elements.append(tabla_cliente)
        elements.append(Spacer(1, padding))
        elements.append(tabla_articulos)
        elements.append(Spacer(1, padding))
        elements.append(tabla_total)
        elements.append(Spacer(1, padding))
        if index + 1< pedidos_count:
            elements.append(PageBreak())
    
    page_height = (max(cantidad_articulos ) * 1.5* cm) + 1*cm
    pdf = SimpleDocTemplate(buffer, pagesize=(8 * cm, page_height), topMargin=0.5 * cm, bottomMargin=0.5 * cm)

    pdf.build(elements)

    pdf_buffer = buffer.getvalue()
    buffer.close()
    from datetime import datetime
    fecha_del_dia = str(datetime.now().date())
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedidos_{fecha_del_dia}.pdf"'
    return response

def add_quarter_page(canvas, doc):
    canvas.saveState()
    canvas.translate(0, -doc.height)
    canvas.restoreState()
    
def generar_pdf_pedido(request, pedido_id):
    return generar_pdf_pedidos(request, [pedido_id])

from django.views.generic.edit import CreateView, UpdateView
from cliente.models import Cliente

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', 'direccion', 'telefono']
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nombre', 'direccion', 'telefono']
    success_url = reverse_lazy('cliente_list')
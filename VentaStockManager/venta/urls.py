from django.urls import re_path, path
from django.conf.urls import handler404

from .views import custom_404_view, redirect_to_ventas
handler404 = custom_404_view

from venta.views import (
    venta_detalle, ventas_por_vendedor, calcular_ganancia_articulos, comprovante_de_venta, ver_pedido, 
    ArticuloAutocomplete, ventas_recientes_por_vendedor, ventas_mensual_por_vendedor, generar_pdf_pedido, generar_pdf_pedidos

)
from .views import ClienteCreateView, ClienteUpdateView

urlpatterns = [
    re_path(
            r'^venta/(?P<venta_id>\d+)/detalle_de_venta',
            venta_detalle,
            name='venta_detalle'),
    re_path(
            r'^ventas_por_vendedor/(?P<id_vendedor>\d+)/$',
             ventas_por_vendedor, 
             name='ventas_por_vendedor'),
    re_path(
            r'^ventas_recientes_por_vendedor/(?P<id_vendedor>\d+)/$',
             ventas_recientes_por_vendedor, 
             name='ventas_recientes_por_vendedor'),    
    re_path(
            r'^ventas_mensual_por_vendedor/(?P<id_vendedor>\d+)/$',
             ventas_mensual_por_vendedor, 
             name='ventas_mensual_por_vendedor'),    

    path('ganancia_por_articulos/', calcular_ganancia_articulos, name='ganancia_por_articulos'),    
    path('articulo-autocomplete/', ArticuloAutocomplete.as_view(), name='articulo-autocomplete'),
    path('venta/<int:venta_id>/', comprovante_de_venta, name='comprovante_de_venta'),
    path('venta/pedido/<int:pedido_id>/', ver_pedido, name='ver_pedido'),
    path('pedido/generar-pdf/<int:pedido_id>', generar_pdf_pedido, name='generar_pdf_pedido'),
    path('cliente/add/', ClienteCreateView.as_view(), name='cliente_add'),
    path('cliente/<int:pk>/edit/', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('venta/pedido/generar-pdfs/', generar_pdf_pedidos, name='generar_pdf_pedidos'),
    path('admin/venta/', redirect_to_ventas, name='redirect_to_ventas'),
]
# url(r'^/(?P<venta_id>\d+)/detalle/$', views.venta_detalle, name='category-detail'),

  
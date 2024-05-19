from django.urls import re_path, path
from django.conf.urls import handler404

from .views import custom_404_view
handler404 = custom_404_view

from venta.views import (
    venta_detalle, ventas_por_vendedor, calcular_ganancia_articulos, comprovante_de_venta, ver_pedido, ArticuloAutocomplete

)

urlpatterns = [
    re_path(
            r'^venta/(?P<venta_id>\d+)/detalle_de_venta',
            venta_detalle,
            name='venta_detalle'),
    re_path(
            r'^ventas_por_vendedor/(?P<id_vendedor>\d+)/$',
             ventas_por_vendedor, 
             name='ventas_por_vendedor'),    
    path('ganancia_por_articulos/', calcular_ganancia_articulos, name='ganancia_por_articulos'),    
    path('articulo-autocomplete/', ArticuloAutocomplete.as_view(), name='articulo-autocomplete'),
    path('venta/<int:venta_id>/', comprovante_de_venta, name='comprovante_de_venta'),
    path('venta/pedido/<int:pedido_id>/', ver_pedido, name='ver_pedido'),


            ]
# url(r'^/(?P<venta_id>\d+)/detalle/$', views.venta_detalle, name='category-detail'),

  
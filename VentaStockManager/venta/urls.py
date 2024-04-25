from django.urls import re_path, path
from venta.views import (
    venta_detalle, ventas_por_vendedor, calcular_ganancia_articulos,

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
    
            ]
# url(r'^/(?P<venta_id>\d+)/detalle/$', views.venta_detalle, name='category-detail'),

  
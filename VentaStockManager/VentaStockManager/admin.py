from django.contrib import admin
from venta.admin import VentaAdmin, PedidoAdmin
from articulo.admin import ArticuloAdmin
from cliente.admin import ClienteAdmin
from compra.admin import ProvedorAdmin, CompraAdmin
from venta.models import Venta, Pedido
from articulo.models import Articulo
from cliente.models import Cliente
from compra.models import Proveedor, Compra


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        # Ensure app_dict values are dictionaries with a "name" key
        for app in app_dict.values():
            if not isinstance(app, dict) or "name" not in app:
                raise ValueError("Invalid app_dict structure")
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        return app_list

admin_site = MyAdminSite()

admin_site.site_header = 'Administrador Osvaldo'
admin_site.index_title = 'Osvaldo Administrador'
admin_site.site_title = 'Osvaldo Programs'
admin_site.register(Venta, VentaAdmin)
admin_site.register(Pedido, PedidoAdmin)
admin_site.register(Articulo, ArticuloAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Proveedor, ProvedorAdmin)
admin_site.register(Compra, CompraAdmin)

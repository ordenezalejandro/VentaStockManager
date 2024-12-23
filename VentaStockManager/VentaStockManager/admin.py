from material.admin.sites import MaterialAdminSite
from venta.admin import VentaAdmin, PedidoAdmin
from articulo.admin import ArticuloAdmin
from cliente.admin import ClienteAdmin
from compra.admin import ProvedorAdmin, CompraAdmin
from venta.models import Venta, Pedido
from articulo.models import Articulo
from cliente.models import Cliente
from compra.models import Proveedor, Compra
from django.apps import apps
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
import logging
from factura_config.models import FacturaConfiguration
from factura_config.admin import FacturaConfigurationAdmin


class MyAdminSite(MaterialAdminSite):
    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)

        
        valid_apps = []
        for app in app_dict.values():
            if not isinstance(app, dict) or "name" not in app:
                logging.error(f"Invalid app_dict structure: {app}")
                continue
            valid_apps.append(app)
        
        app_list = sorted(valid_apps, key=lambda x: x["name"].lower())
        
        # Add icons to the app list
        for app in app_list:
            app_config = apps.get_app_config(app['app_label'])
            app['icon'] = getattr(app_config, 'icon_name', 'default_icon')
        
        return app_list
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

UserAdmin.icon_name = "person"

admin_site = MyAdminSite()

admin_site.site_header = format_html(
    'Osvaldo Administrator - <span class="text-primary">Precios<button class="btn btn-primary" onclick="window.location.href=\'https://jairodo.pythonanywhere.com/lista_precios\'"><a class="pl-4 ml-4 material-icons" title="Ir a la lista de precios">arrow_forward</a></button><button class="btn btn-secondary" onclick="navigator.clipboard.writeText(\'https://jairodo.pythonanywhere.com/lista_precios\')"><a class="mb-2 material-icons" title="Copiar link lista de precios">content_copy</a></button></span>'
)
admin_site.index_title = 'Osvaldo Administrador '
admin_site.site_title = 'Osvaldo Programs'

admin_site.register(User, UserAdmin)
admin_site.register(Venta, VentaAdmin)
admin_site.register(Pedido, PedidoAdmin)
admin_site.register(Articulo, ArticuloAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Proveedor, ProvedorAdmin)
admin_site.register(Compra, CompraAdmin)
admin_site.register(FacturaConfiguration, FacturaConfigurationAdmin)
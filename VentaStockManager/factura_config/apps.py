from django.apps import AppConfig


class FacturaConfigConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "factura_config"
    icon_name = "receipt"
    verbose_name = "Configuración de facturas"
from django.contrib import admin
from .models import FacturaConfiguration

class FacturaConfigurationAdmin(admin.ModelAdmin):
    model = FacturaConfiguration
    icon_name = "receipt"
    fieldsets = (
        ('Dimensiones de página', {
            'fields': ('page_width',)
        }),
        ('Márgenes', {
            'fields': ('margin_top', 'margin_bottom', 'margin_left', 'margin_right')
        }),
        ('Fuentes', {
            'fields': ('header_font', 'content_font', "total_font",
                      'font_size_header', 'font_size_content', 'font_size_total')
        }),
        ('Colores', {
            'fields': ('header_color', 'content_color', 'table_border_color')
        }),
        ('Estilos de tabla', {
            'fields': ('table_border_width',)
        }),
        ('Anchos de columna', {
            'fields': ('column_width_article', 'column_width_quantity',
                      'column_width_price', 'column_width_total')
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True
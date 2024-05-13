from django.contrib import admin
# Register your models here.
from vendedor.models import Vendedor
from django.urls import reverse
from django.utils.html import format_html

class VendedorAdmin(admin.ModelAdmin):
    icon_name = "phone_android"
    model = Vendedor
    search_fields = ('nombre', 'apellido')
    
    def ventas_por_vendedor(self, obj):
        """
        Proporciona un enlace para ver las ventas por vendedor.
        """
        url = reverse('ventas_por_vendedor', args=[obj.id])
        return format_html('<a href="{}">Ver Ventas</a>', url)
    
    list_display = ['nombre', 'apellido', 'ventas_por_vendedor']

    ventas_por_vendedor.short_description = 'Ventas por Vendedor'


    readonly_fields = ['ventas_por_vendedor',]

admin.site.register(Vendedor, VendedorAdmin)
from django.contrib import admin

from .models import Proveedor, Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1  # Allows adding one extra detail by default

class CompraAdmin(admin.ModelAdmin):
    inlines = [DetalleCompraInline]

admin.site.register(Proveedor)

admin.site.register(Compra, CompraAdmin)
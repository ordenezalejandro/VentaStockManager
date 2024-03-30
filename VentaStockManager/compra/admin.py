from django.contrib import admin
#from .forms import CompraAdminForm


from .models import Proveedor, Compra, DetalleCompra

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1  # Allows adding one extra detail by default

class CompraAdmin(admin.ModelAdmin):
    inlines = [DetalleCompraInline]

admin.site.register(Proveedor)

admin.site.register(Compra, CompraAdmin)


#@admin.register(Compra)
#lass CompraAdmin(admin.ModelAdmin):
  #  form = CompraAdminForm
####



from django.contrib import admin
# Register your models here.
from vendedor.models import Vendedor

class VendedorAdmin(admin.ModelAdmin):
    icon_name = "phone_android"
    model = Vendedor
    search_fields = ('nombre', 'apellido')

admin.site.register(Vendedor, VendedorAdmin)
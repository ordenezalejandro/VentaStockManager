# from django.contrib import admin
import autocomplete_all as admin
# Register your models here.
from vendedor.models import Vendedor

class VendedorAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido')

admin.site.register(Vendedor, VendedorAdmin)
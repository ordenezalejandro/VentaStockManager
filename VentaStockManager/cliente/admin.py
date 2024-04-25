# from django.contrib import admin
from cliente.models import Cliente
import autocomplete_all as admin

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido')

admin.site.register(Cliente, ClienteAdmin)
# Register your models here.

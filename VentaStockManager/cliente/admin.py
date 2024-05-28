from django.contrib import admin
from cliente.models import Cliente
from django.contrib.auth.models import  Group

from .models import Cliente


# admin.site.register(Cliente)
# Register your models here.



# Registra el modelo Cliente en el administrador de Djang

class ClienteAdmin(admin.ModelAdmin):
   icon_name = "account_circle"
   model = Cliente
   search_fields = ['nombre']
   list_display = ('nombre_completo', 'telefono')
    
admin.register(Cliente, ClienteAdmin)
# Desregistrar otros modelos que no necesitan administración en el panel de administración
admin.site.register(Cliente, ClienteAdmin)


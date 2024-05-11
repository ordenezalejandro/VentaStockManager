from django.contrib import admin
from cliente.models import Cliente
from django.contrib.auth.models import Permission, Group

from .models import Cliente


# admin.site.register(Cliente)
# Register your models here.



# Registra el modelo Cliente en el administrador de Django

class ClienteAdmin(admin.ModelAdmin):
   icon_name = "account_circle"
   model = Cliente


   list_display = ('nombre_completo', 'telefono')
    
   
    # Esta función se llama cuando se guarda un nuevo objeto Cliente en el administrador
   def save_model(self, request, obj, form, change):
        # Asigna el permiso de "Puede ver tus artículos" al nuevo cliente creado
        obj.user.user_permissions.add(Permission.objects.get(codename='view_your_items'))

admin.register(Cliente, ClienteAdmin)
# Desregistrar otros modelos que no necesitan administración en el panel de administración
admin.site.register(Cliente, ClienteAdmin)
admin.site.unregister(Group)

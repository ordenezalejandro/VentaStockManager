# app/management/commands/cargar_clientes.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Cargar clientes en la base de datos'

    def handle(self, *args, **kwargs):
        clientes_data = [
            {
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'cuil': 12345678901,
                'telefono': '1234567890',
                'edad': 30,
                'sexo': 'M'
            },
            {
                'nombre': 'María',
                'apellido': 'González',
                'cuil': 12345678902,
                'telefono': '1234567891',
                'edad': 25,
                'sexo': 'F'
            },
            {
                'nombre': 'Carlos',
                'apellido': 'Martínez',
                'cuil': 12345678903,
                'telefono': '1234567892',
                'edad': 35,
                'sexo': 'M'
            },
            # Agrega más clientes según sea necesario
        ]

        for cliente_data in clientes_data:
            # Crea el usuario
            usuario = User.objects.create_user(
                username=cliente_data['nombre'].lower(),
                first_name=cliente_data['nombre'],
                last_name=cliente_data['apellido'],
            )
            
            # Crea el cliente
            Cliente.objects.create(
                nombre=cliente_data['nombre'],
                apellido=cliente_data['apellido'],
                perfil=usuario,
                cuil=cliente_data['cuil'],
                telefono=cliente_data['telefono'],
                edad=cliente_data['edad'],
                sexo=cliente_data['sexo']
            )

        self.stdout.write(self.style.SUCCESS('Clientes cargados exitosamente.'))

        

        self.stdout.write(self.style.SUCCESS(f'Cliente creado: {cliente}'))

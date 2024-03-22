from django.core.management.base import BaseCommand
from vendedor.models import Vendedor

class Command(BaseCommand):
    help = 'Carga vendedores en la base de datos desde un script'

    def handle(self, *args, **kwargs):
        # Datos de ejemplo de vendedores
        vendedores = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'cuil': 12345678901, 'telefono': '1234567890', 'edad': 30, 'sexo': 'M'},
            {'nombre': 'María', 'apellido': 'González', 'cuil': 12345678902, 'telefono': '1234567891', 'edad': 25, 'sexo': 'F'},
            {'nombre': 'Carlos', 'apellido': 'Martínez', 'cuil': 12345678903, 'telefono': '1234567892', 'edad': 35, 'sexo': 'M'},
            {'nombre': 'Ana', 'apellido': 'López', 'cuil': 12345678904, 'telefono': '1234567893', 'edad': 28, 'sexo': 'F'},
            {'nombre': 'Pedro', 'apellido': 'Rodríguez', 'cuil': 12345678905, 'telefono': '1234567894', 'edad': 40, 'sexo': 'M'},
        ]

        # Guarda los vendedores en la base de datos
        for vendedor_data in vendedores:
            vendedor = Vendedor(**vendedor_data)
            vendedor.full_clean()  # Realiza validaciones del modelo
            vendedor.save()

        self.stdout.write(self.style.SUCCESS('Vendedores cargados exitosamente'))

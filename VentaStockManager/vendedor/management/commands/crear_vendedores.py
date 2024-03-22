from django.core.management.base import BaseCommand
from vendedor.models import Vendedor

class Command(BaseCommand):
    help = 'Carga vendedores en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('nombre', type=str, help='Nombre del vendedor')
        parser.add_argument('apellido', type=str, help='Apellido del vendedor')
        parser.add_argument('cuil', type=int, help='CUIL del vendedor')
        parser.add_argument('telefono', type=str, help='Teléfono del vendedor')
        parser.add_argument('edad', type=int, help='Edad del vendedor')
        parser.add_argument('sexo', type=str, help='Sexo del vendedor (M/F)')

    def handle(self, *args, **kwargs):
        nombre = kwargs['nombre']
        apellido = kwargs['apellido']
        cuil = kwargs['cuil']
        telefono = kwargs['telefono']
        edad = kwargs['edad']
        sexo = kwargs['sexo']

        vendedor = Vendedor(nombre=nombre, apellido=apellido, cuil=cuil, telefono=telefono, edad=edad, sexo=sexo)
        vendedor.full_clean()  # Realiza validaciones del modelo
        vendedor.save()

        self.stdout.write(self.style.SUCCESS(f'Vendedor creado: {vendedor}'))

     
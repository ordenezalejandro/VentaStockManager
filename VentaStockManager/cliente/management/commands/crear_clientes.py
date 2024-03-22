from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Agrega clientes con nombre, apellido, CUIL y teléfono'

    def add_arguments(self, parser):
        parser.add_argument('nombre', type=str, help='Nombre del cliente')
        parser.add_argument('apellido', type=str, help='Apellido del cliente')
        parser.add_argument('cuil', type=int, help='CUIL del cliente')
        parser.add_argument('telefono', type=str, help='Teléfono del cliente')
        parser.add_argument('edad', type=int, help='Edad del cliente')
        parser.add_argument('sexo', type=str, help='Sexo del cliente')

    def handle(self, *args, **options):
        nombre = options['nombre']
        apellido = options['apellido']
        cuil = options['cuil']
        telefono = options['telefono']
        edad = options['edad']
        sexo = options['sexo']
        
        # Crear el usuario
        usuario = User.objects.create_user(
            username=nombre.lower(),
            first_name=nombre,
            last_name=apellido,
        )
        
        # Crear el cliente
        cliente = Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            perfil=usuario,
            cuil=cuil,
            telefono=telefono,
            edad=edad,
            sexo=sexo,
        )

        self.stdout.write(self.style.SUCCESS(f'Cliente creado: {cliente}'))

import random
import string
from datetime import timedelta
from django.core.management.base import BaseCommand
from articulo.models import Articulo

class Command(BaseCommand):
    help = 'Cargar varios artículos desde un script'

    def sugerir_codigo_interno(self, articulo_data):
        marca = articulo_data['marca']
        nombre = articulo_data['nombre']
        # Obtener las iniciales del nombre del artículo
        iniciales_nombre = ''.join(word[0] for word in nombre.split())
        # Generar un número aleatorio de 4 dígitos
        numero_aleatorio = ''.join(random.choices(string.digits, k=4))
        # Combinar la marca, iniciales y número aleatorio
        codigo_interno = f'{marca}_{iniciales_nombre}_{numero_aleatorio}'
        return codigo_interno

    def handle(self, *args, **options):
        # Lista de artículos para cargar
        articulos_para_cargar = [
            {
                'codigo': 1001,
                'nombre': 'Chupetines de colores',
                'descripcion': 'Bolsa de chupetines de colores surtidos.',
                'precio_compra': 0.50,
                'precio_venta': 1.00,
                'stock': 100,
                'precio_minorista': 1.50,
                'precio_mayorista': 1.00,
                'vencimiento': timedelta(days=90),  # Vencimiento mayor a 60 días (90 días)
                'marca': 'juspy',  # Agregar marca
            },
            {
                'codigo': 1002,
                'nombre': 'Bolsa de caramelos surtidos',
                'descripcion': 'Bolsa de caramelos con distintos sabores.',
                'precio_compra': 0.75,
                'precio_venta': 1.50,
                'stock': 80,
                'precio_minorista': 1.80,
                'precio_mayorista': 1.20,
                'vencimiento': timedelta(days=70),  # Vencimiento mayor a 60 días (70 días)
                'marca': 'flimpaf',  # Agregar marca
            },
            # Agregar los otros artículos con los atributos de marca
        ]

        # Iterar sobre la lista de artículos y crear cada uno
        for articulo_data in articulos_para_cargar:
            # Obtener sugerencia para el código interno
            articulo_data['codigo_interno'] = self.sugerir_codigo_interno(articulo_data)
            articulo = Articulo(**articulo_data)
            articulo.save()

        self.stdout.write(self.style.SUCCESS('Se han cargado los artículos correctamente.'))

       
      
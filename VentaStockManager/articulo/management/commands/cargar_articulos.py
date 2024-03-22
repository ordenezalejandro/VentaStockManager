import datetime
from django.core.management.base import BaseCommand
from articulo.models import Articulo

class Command(BaseCommand):
    help = 'Carga artículos en la base de datos'

    def handle(self, *args, **kwargs):
        articulos_data = [
            {
                'codigo': 1,
                'nombre': 'Artículo 1',
                'descripcion': 'Descripción del Artículo 1',
                'precio_compra': 10.50,
                'precio_venta': 15.00,
                'stock': 100,
                'precio_minorista': 12.00,
                'precio_mayorista': 10.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=30)
            },
            {
                'codigo': 2,
                'nombre': 'Artículo 2',
                'descripcion': 'Descripción del Artículo 2',
                'precio_compra': 15.25,
                'precio_venta': 20.00,
                'stock': 50,
                'precio_minorista': 18.00,
                'precio_mayorista': 15.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=45)
            },
            {
                'codigo': 3,
                'nombre': 'Artículo 3',
                'descripcion': 'Descripción del Artículo 3',
                'precio_compra': 20.00,
                'precio_venta': 25.00,
                'stock': 80,
                'precio_minorista': 22.00,
                'precio_mayorista': 18.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=60)
            },
            {
                'codigo': 4,
                'nombre': 'Artículo 4',
                'descripcion': 'Descripción del Artículo 4',
                'precio_compra': 8.75,
                'precio_venta': 12.00,
                'stock': 120,
                'precio_minorista': 10.00,
                'precio_mayorista': 8.50,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=20)
            },
            {
                'codigo': 5,
                'nombre': 'Artículo 5',
                'descripcion': 'Descripción del Artículo 5',
                'precio_compra': 12.00,
                'precio_venta': 18.00,
                'stock': 60,
                'precio_minorista': 14.00,
                'precio_mayorista': 11.50,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=40)
            }
        ]

        for articulo_data in articulos_data:
            articulo = Articulo(**articulo_data)
            articulo.save()

        self.stdout.write(self.style.SUCCESS('Se han cargado los artículos correctamente.'))

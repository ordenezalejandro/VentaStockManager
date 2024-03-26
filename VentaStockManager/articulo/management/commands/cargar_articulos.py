import datetime
from django.core.management.base import BaseCommand
from articulo.models import Articulo

class Command(BaseCommand):
    help = 'Carga artículos en la base de datos'

    def handle(self, *args, **kwargs):
        articulos_data = [
            {
                'codigo': 1,
                'nombre': 'galletas',
                'descripcion': 'galletas de chocolate',
                'precio_compra': 10.50,
                'precio_venta': 15.00,
                'stock': 100,
                'precio_minorista': 12.00,
                'precio_mayorista': 10.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=30)
            },
            {
                'codigo': 2,
                'nombre': 'alfajores',
                'descripcion': 'alfajor 3 tapas',
                'precio_compra': 15.25,
                'precio_venta': 20.00,
                'stock': 50,
                'precio_minorista': 18.00,
                'precio_mayorista': 15.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=45)
            },
            {
                'codigo': 3,
                'nombre': 'cupetin',
                'descripcion': 'chupetin con chicle',
                'precio_compra': 20.00,
                'precio_venta': 25.00,
                'stock': 80,
                'precio_minorista': 22.00,
                'precio_mayorista': 18.00,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=60)
            },
            {
                'codigo': 4,
                'nombre': 'caramelos',
                'descripcion': 'caramelos masticables',
                'precio_compra': 8.75,
                'precio_venta': 12.00,
                'stock': 120,
                'precio_minorista': 10.00,
                'precio_mayorista': 8.50,
                'vencimiento': datetime.date.today() + datetime.timedelta(days=20)
            },
            {
                'codigo': 5,
                'nombre': 'jugos',
                'descripcion': 'jugos tang',
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

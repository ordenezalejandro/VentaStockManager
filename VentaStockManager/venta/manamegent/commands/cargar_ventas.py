`import datetime
from django.core.management.base import BaseCommand
from venta.models import Venta, ArticuloVenta, Cliente, Vendedor, Articulo

class Command(BaseCommand):
    help = 'Carga ventas en la base de datos'

    def handle(self, *args, **kwargs):
        # Obtener objetos Cliente y Vendedor de ejemplo
        cliente = Cliente.objects.first()  # Obtener el primer cliente en la base de datos
        vendedor = Vendedor.objects.figitrst()  # Obtener el primer vendedor en la base de datos

        # Datos de ventas (puedes cambiar estos datos según tus necesidades)
        ventas_data = [
            {
                'fecha_compra': datetime.date.today(),
                'fecha_entrega': datetime.date.today() + datetime.timedelta(days=7),
                'articulos': [
                    {
                        'articulo': Articulo.objects.get(codigo=1),  # Obtener el artículo por su código
                        'cantidad': 2,
                        'precio_minorista': 15.00,
                        'precio_mayorista': 12.00
                    },
                    {
                        'articulo': Articulo.objects.get(codigo=2),
                        'cantidad': 3,
                        'precio_minorista': 20.00,
                        'precio_mayorista': 18.00
                    }
                    # Puedes agregar más artículos a la venta aquí
                ]
            }
            # Puedes agregar más ventas aquí
        ]

        for venta_data in ventas_data:
            # Crear la venta
            venta = Venta.objects.create(
                fecha_compra=venta_data['fecha_compra'],
                fecha_entrega=venta_data['fecha_entrega'],
                cliente=cliente,
                Vendedor=vendedor
            )

            # Crear los ArticulosVenta asociados a la venta
            for articulo_info in venta_data['articulos']:
                articulo_venta = ArticuloVenta.objects.create(
                    venta=venta,
                    articulo=articulo_info['articulo'],
                    cantidad=articulo_info['cantidad'],
                    precio_minorista=articulo_info['precio_minorista'],
                    precio_mayorista=articulo_info['precio_mayorista']
                )

        self.stdout.write(self.style.SUCCESS('Se han cargado las ventas correctamente.'))
`
from django.test import TestCase
import factory
from pprint import pprint
from venta.models import Venta, ArticuloVenta
from compra.models import Compra, Proveedor, DetalleCompra
from cliente.models import Cliente
from vendedor.models import Vendedor
from articulo.models import Articulo
from django.contrib.auth.models import User
from faker import Faker

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.email())

class ProveedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Proveedor

    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    direccion = factory.Faker('street_address')
    telefono = factory.Faker('phone_number')
    email = factory.LazyAttribute(lambda o: f"{o.nombre.lower()}.{o.apellido.lower()}@example.com")
    perfil = factory.SubFactory(UserFactory)

class ArticuloFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Articulo

    nombre = factory.Faker('word')
    descripcion = factory.Faker('paragraph')
    precio_unitario = factory.Faker('random_number', digits=2)

class CompraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Compra

    fecha_compra = factory.Faker('date_this_decade')
    proveedor = factory.SubFactory(ProveedorFactory)

class DetalleCompraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DetalleCompra

    compra = factory.SubFactory(CompraFactory)
    articulo = factory.SubFactory(ArticuloFactory)
    cantidad = factory.Faker('random_number', digits=1)
    precio_unitario = factory.Faker('random_number', digits=2)
class ClienteFactory(factory.Factory):
    class Meta:
        model = Cliente

    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name') 
    perfil = factory.SubFactory(UserFactory)

class VendedorFactory(factory.Factory):
    class Meta:
        model = Vendedor
    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    perfil = factory.SubFactory(UserFactory)


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    # Otros campos de cliente si los hubiera

class VendedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendedor

    nombre = factory.Faker('first_name')
    apellido = factory.Faker('last_name')
    # Otros campos de vendedor si los hubiera

class VentaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venta

    fecha_compra = factory.Faker('date_between', start_date='-30d', end_date='today')
    fecha_entrega = factory.Faker('date_between', start_date='today', end_date='+30d')
    cliente = factory.SubFactory(ClienteFactory)
    vendedor = factory.SubFactory(VendedorFactory)

class ArticuloVentaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticuloVenta

    venta = factory.SubFactory(VentaFactory)
    articulo = factory.SubFactory(ArticuloFactory)  # Utiliza el factory de Articulo previamente definido
    cantidad = factory.Faker('random_int', min=1, max=10)
    precio_minorista = factory.Faker('random_number', digits=2)

# Create your tests here.
class CalcularGananciaPorArticuloTestCase(TestCase):
#     def setUp(self): 
#         self.cliente = baker.make('c3liente.Cliente')
#         self.compra = baker.make("compra.Compra")
#         pprint(self.cliente.__dict__)

    def test_calcular_ganancia(self):
        articulo1 = Articulo.objects.create(nombre="Artículo 1")
        articulo2 = Articulo.objects.create(nombre="Artículo 2")
        compra_inicial = CompraFactory.create()

        compra_detalle1 = CompraDetalle.create(compra=compra_inical, articulo=articulo1, cantidad=3)
        # Creamos una compra con 4 artículos
        venta1 = VentaFactory.create()
        ArticuloVentaFactory.create(venta=venta1, articulo=articulo1, cantidad=2)
        ArticuloVentaFactory.create(venta=venta1, articulo=articulo2, cantidad=2)

        # Creamos otra compra con 2 artículos, de los cuales uno es el mismo del primer pedido
        venta2 = VentaFactory.create()
        ArticuloVentaFactory.create(venta=venta2, articulo=articulo1, cantidad=1)
        ArticuloVentaFactory.create(venta=venta2, articulo=articulo2, cantidad=1)

        # hacer compra. de 4 productos distintos
        # despues hacer 1 venta que venta venda todo
        # luego comparar el stock de cada articulo. deberia ser cero
        # luego contar la ganacia. deberia ser el total de la venta - el total de la compra
        # compra =  mommy.make('compra.models.compra')

from django.test import TestCase
from  .models import Articulo
# Create your tests here.


class TestUtils(TestCase):
    def test_sugerir_codigo_interno(self):
        articulo1 = Articulo(nombre="Caja de Chupetines Chicles", marca="bagley")
        nombre_sugerido =  articulo1.sugerir_codigo_interno()
        nombre_sugerido_esperado = "bagleycdcc"
        self.assertEquals(nombre_sugerido[:len(nombre_sugerido_esperado)] == nombre_sugerido_esperado, "el nombre sugerido no es correcto")
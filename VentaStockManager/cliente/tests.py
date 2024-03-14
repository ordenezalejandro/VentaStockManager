from django.test import TestCase
from cliente.models import Cliente
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class MyClientUrlTests(TestCase):
    def test_filtrar_por_mayor(self):
        # Define the URL to test
        perfil_1 = User(email='email@test.com', password='12345', username='per1')
        cliente_1 = Cliente(nombre='test1', apellido='ordonez',perfil=perfil_1, edad=18, cuil='234234234')
        perfil_1.save()
        cliente_1.save()
        perfil_2 = User(email='emai2l@test.com', password='12345')
        cliente_2 = Cliente(nombre='test2', apellido='ordonez2',perfil=perfil_2, edad=16, cuil='123123123')
        url_to_test = reverse('filtrar_por_mayor_de_edad')  # Replace 'my_view_name' with the actual view name

        perfil_2.save()
        cliente_2.save()
        
        # Simulate a GET request on the URL
        response = self.client.get(url_to_test)
        
        # Assert the expected response status code
        self.assertEqual(response.status_code, 200)
        # import pdb
        # pdb.set_trace()
        self.assertIn('Clientes mayores de edad:', str(response.content))
        self.assertIn(f'Cliente:{cliente_1.nombre} {cliente_1.apellido} ({cliente_1.edad}', str(response.content))
        self.assertNotIn(f'Cliente:{cliente_2.nombre} {cliente_2.apellido} ({cliente_2.edad}', str(response.content))
import os
import django

# Configura la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VentaStockManager.settings')
django.setup()

from vendedor.models import Vendedor

def cargar_datos():
    # Datos de los vendedores
    vendedores = [
        {'nombre': 'Juan', 'apellido': 'Pérez', 'cuil': 12345678901, 'telefono': '1234567890', 'edad': 30, 'sexo': 'M'},
        {'nombre': 'María', 'apellido': 'González', 'cuil': 12345678902, 'telefono': '1234567891', 'edad': 25, 'sexo': 'F'},
        {'nombre': 'Carlos', 'apellido': 'Martínez', 'cuil': 12345678903, 'telefono': '1234567892', 'edad': 35, 'sexo': 'M'},
        {'nombre': 'Ana', 'apellido': 'López', 'cuil': 12345678904, 'telefono': '1234567893', 'edad': 28, 'sexo': 'F'},
    ]

    # Guarda los vendedores en la base de datos
    for vendedor_data in vendedores:
        vendedor = Vendedor(**vendedor_data)
        vendedor.full_clean()  # Realiza validaciones del modelo
        vendedor.save()

    print("Datos cargados exitosamente")

if __name__ == '__main__':
    cargar_datos()


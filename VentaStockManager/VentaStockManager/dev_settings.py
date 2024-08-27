from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
# Application definition    
INSTALLED_APPS = [
    'material',
    # 'material.admin',
    # 'material.admin.default',
    # 'whitenoise.runserver_nostatic',    
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'bootstrap5',
    'dal',
    'dal_select2',
    'django_extensions',
    'cliente.apps.ClienteConfig',
    'venta.apps.VentaConfig',
    'articulo.apps.ArticuloConfig',
    'vendedor.apps.VendedorConfig',
    'compra.apps.CompraConfig',
]

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# WHITENOISE_MANIFEST_STRICT = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'articulo', 'static'),
]
# STATICFILES_STORAGE =('whitenoise.storage.CompressedManifestStaticFilesStorage')

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Quick-start development settings - unsuitable for production
SECRET_KEY = "DihCl2FfbgQqgUDEp0HS_aJPqcSUlP_lB_HytyBi29Ws791ZTNgaWqgK9LNp9SANpXM"
# CSRF_COOKIE_SECURE = True
# # Configuración para hacer que las cookies de sesión solo se envíen a través de conexiones seguras
# SESSION_COOKIE_SECURE = True
# DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))
DEBUG=False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '2ee0-201-252-61-204.ngrok-free.app', 'jairoDO.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ["https://2ee0-201-252-61-204.ngrok-free.app"]

# Application definition    
INSTALLED_APPS = [
    'material',
    'material.admin',
    # 'material.admin.default',
    'whitenoise.runserver_nostatic',    
    'django.contrib.auth',
    #'django.contrib.admin'
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'bootstrap5',
    'dal',
    'dal_select2',
    'django_extensions',
    'cliente.apps.ClienteConfig',
    'venta.apps.VentaConfig',
    'articulo.apps.ArticuloConfig',
    'vendedor.apps.VendedorConfig',
    'compra.apps.CompraConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'VentaStockManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'compra', 'templates'),
            os.path.join(BASE_DIR, 'venta', 'templates'),
            os.path.join(BASE_DIR, 'cliente', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# # Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jairoDO$osvaldo_manager',
        'USER': 'jairoDO',
        'PASSWORD': '05v4ld0!',
        'HOST': 'jairoDO.mysql.pythonanywhere-services.com',
        'PORT': '3306'
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
# USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Additional settings
ADMIN_MEDIA_PREFIX = '/static/admin/'

MATERIAL_ADMIN_SITE = {
    # 'HEADER':  _('Your site header'),  # Admin site header
    # 'TITLE':  _('Your site title'),  # Admin site title
    # 'FAVICON':  'path/to/favicon',  # Admin site favicon (path to static should be specified)
    # 'MAIN_BG_COLOR':  'color',  # Admin site main color, css color should be specified
    # 'MAIN_HOVER_COLOR':  'color',  # Admin site main hover color, css color should be specified
    # 'PROFILE_PICTURE':  'path/to/image',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG':  'path/to/image',  # Admin site profile background (path to static should be specified)
    # 'LOGIN_LOGO':  'path/to/image',  # Admin site logo on login page (path to static should be specified)
    # 'LOGOUT_BG':  'path/to/image',  # Admin site background on login/logout pages (path to static should be specified)
    'SHOW_THEMES':  True,  #  Show default admin themes button
    'TRAY_REVERSE': True,  # Hide object-tools and additional-submit-line by default
    'NAVBAR_REVERSE': True,  # Hide side navbar by default
    'SHOW_COUNTS': True, # Show instances counts for each model
    'APP_ICONS': {  # Set icons for applications(lowercase), including 3rd party apps, {'application_name': 'material_icon_name', ...}
        'sites': 'send',
    },
    'MODEL_ICONS': {  # Set icons for models(lowercase), including 3rd party models, {'model_name': 'material_icon_name', ...}
        'site': 'contact_mail',
    }
}
# settings.py

# Configuración de HSTS (HTTP Strict Transport Security)
# SECURE_HSTS_SECONDS = 31536000  # 1 año en segundos
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_PRELOAD = True
# Asegúrate de leer la documentación y ajustar el valor según tus necesidades de seguridad
if DEBUG:

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

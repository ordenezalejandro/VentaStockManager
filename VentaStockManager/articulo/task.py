import os
# from django_q.tasks import async_task
from django.core.management import call_command
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import datetime, timedelta
from articulo.models import Articulo
import traceback
import decimal
import openpyxl
# from django_q.tasks import async_task
directorio_credenciales = 'credentials_module.json'
file_id = '1Zv9TDVJRDG_Ar-U4qTvlTcTiJ7RUpZnawxGwPpL4IZI'
mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VentaStockManager.settings')

def login_google_drive():
    gauth = GoogleAuth()
    gauth.settings['get_refresh_token'] = True  # Asegúrate de obtener el refresh token
    gauth.settings['client_config_file'] = 'client_secrets.json'
    gauth.settings['get_refresh_token'] = True
    gauth.settings['oauth_scope'] = ['https://www.googleapis.com/auth/drive']
    gauth.settings['access_type'] = 'offline'
    gauth.LoadCredentialsFile(directorio_credenciales)  # Corrige el error tipográfico
    
    if gauth.access_token_expired:
        try:
            gauth.Refresh()  # Intenta refrescar el token
        except Exception as e:
            print(f"Error al refrescar el token: {e}")
            gauth.LocalWebserverAuth()  # Reautentica si no se puede refrescar
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.LoadCredentialsFile(directorio_credenciales)
        gauth.Authorize()
    
    return GoogleDrive(gauth)

def download_file_from_google_drive(id_archivo, ruta_descarga):
    credentials = login_google_drive()
    archivo = credentials.CreateFile({'id': id_archivo})
    nombre_archivo = archivo['title'] + '.xlsx'
    
    # Asegúrate de que la carpeta de destino exista
    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
    
    try:
        archivo.GetContentFile(os.path.join(ruta_descarga, nombre_archivo), mimetype=mime_type)
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None
    
    return os.path.join(ruta_descarga, nombre_archivo)
    
def buscar_y_cargar_documento():
    # Ruta del documento en el driver
    ruta_documento = download_file_from_google_drive(file_id, 'articulo/data/')

    # Verifica si el documento existe
    if ruta_documento and os.path.exists(ruta_documento):
        # Ejecuta el comando cargar_articulo_xlsx
        call_command('cargar_articulo_xlsx','-ruta_archivo', ruta_documento)
    else:
        print(f"Documento no encontrado en {ruta_documento}")

def generar_diccionario_letras_a_enteros():
    letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    diccionario = {letra: indice + 1 for indice, letra in enumerate(letras)}
    return diccionario

DICCIONARIO_DE_LETRAS = generar_diccionario_letras_a_enteros()

def procesar_archivo_xlsx(ruta_archivo):
    errores = []
    wb = openpyxl.load_workbook(ruta_archivo)
    sheet = wb.active
    for i, row in enumerate(sheet.iter_rows(min_row=4, values_only=True)):
        if not row[0] or not row[1] or not row[3] or not row[3] or (row[3]  is str and row[3].replace('$','') == ''):  # Si la primera celda está vacía, saltar la
            if row[1]:
                # self.stdout.write(f'esta fila no se proceso fila {i+4} row {row[0]} {row[1]}')
                errores.append(f'revise la fila {i+4} row {row[0]} {row[1]}')
            continue
        try:
            nombre = row[0]
            codigo_interno = row[1]
            letra = DICCIONARIO_DE_LETRAS[row[1][0].upper()]
            codigo = int(f'{letra}{row[1][1:]}')
            try:
                precio_minorista = decimal.Decimal(row[3].replace('$', ''))
            except:
                # self.stdout.write(self.style.ERROR(f'Error al procesar la fila {i+1}: {str(e)} , se pondra a 0'))
                errores.append(f'Error al procesar la fila {i+1}: {str(e)} , se pondra a 0')
                precio_minorista = 0
            precio_mayorista = round(precio_minorista*decimal.Decimal(0.97), 2)

            precio_mayorista = round(precio_minorista*decimal.Decimal(0.97), 2)

            if not all([nombre, codigo_interno, precio_minorista]):
                pass# self.stdout.write(self.style.ERROR(f'Fila {i+1} no se agregó: nombre, código interno o precio minorista es None.'))            
                errores.append(f'Fila {i+1} no se agregó: nombre, código interno o precio minorista es None.')
        except Exception as e:
            errores.append(f'Error al procesar la fila {i+1}: {str(e)}')
            
            # self.stdout.write(self.style.ERROR(f'Error al procesar la fila {i+1}: {str(e)}'))
            # self.stdout.write(self.style.ERROR(traceback.format_exc()))
            continue

        
            
        # codigo_interno = self.generar_codigo_interno(nombre)

        articulo, creado = Articulo.objects.get_or_create(
            codigo_interno=codigo_interno,
            nombre=nombre,
            defaults={
            'codigo': codigo,
            'stock': 100,
            'vencimiento': datetime.now() + timedelta(days=90)
            }
        )
        articulo.precio_minorista = precio_minorista
        articulo.precio_mayorista = precio_mayorista
        articulo.stock = 100
        if articulo.codigo is None:
            articulo.codigo = codigo_interno
        articulo.stock = 100
        articulo.save()

    return errores  

def actualizar_precios_articulos_desde_drive():
    ruta_archivo = download_file_from_google_drive(file_id, 'articulo/data/')
    if ruta_archivo and os.path.exists(ruta_archivo):
        errores = procesar_archivo_xlsx(ruta_archivo)
        if errores:
            return errores
        else:
            return "Se actualizar los precios desde e archvo drive con exito"
    else:
        return f"Archivo no encontrado en {ruta_archivo}"
def generar_codigo_interno(nombre):
    primera_letra = nombre[0].lower()

    if Articulo.objects.filter(codigo_interno__startswith=primera_letra).exists():
        codigo_interno = nombre[:2].lower()
    else:
        codigo_interno = primera_letra

    return codigo_interno

# Programar la tarea
# async_task('VentaStockManager.tasks.actualizar_precios_articulos_desde_drive')

    
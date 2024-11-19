
import random
import string
from django.db import models
import random
from django.utils.html import format_html
# Create your models here.
class Articulo(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255)
    codigo_interno = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField()
    precio_minorista = models.DecimalField(max_digits=10, decimal_places=2,  null=True)
    precio_mayorista = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vencimiento = models.DateField(blank=True)
    marca = models.CharField(max_length=255, blank=True, null=True, default='Generico')
    cantidad_por_mayor = models.PositiveIntegerField(default=100, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo_interno:
            # Obtener las iniciales del nombre del artículo
            iniciales = ''.join(word[0] for word in self.nombre.split())
            # Generar un número aleatorio de 4 dígitos
            random_number = ''.join(random.choices(string.digits, k=4))
            # Combinar las iniciales y el número aleatorio
            self.codigo_interno = iniciales.upper() + random_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo} - {self.codigo_interno} | {self.marca + " - " if self.marca else " - "} |  {self.nombre}' \
               f' | Min ${self.precio_minorista} | May ${self.precio_mayorista} '\
               f'|umbral {self.cantidad_por_mayor}'
                   

    def get_articulo_short_name(self):
        return  f'{self.codigo_interno} {self.marca if self.marca != "Generico" else ""} {self.nombre}'
    
    def sugerir_codigo_interno(self):
        
        if not self.nombre:
            return self.id
        else:
            iniciales = [palabra[0] for palabra in self.nombre.split() if palabra]
            random_int = [str(random.randint(0, 10) for i in range(3))]
            return ''.join(iniciales + random_int)

    class Meta:
        ordering = ['codigo']
            
  
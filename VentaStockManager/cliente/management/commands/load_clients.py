import re
from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Carga clientes desde un texto proporcionado'

    DAYS_MAPPING = {
        'LUNES': 'l',
        'MARTES': 'ma',
        'MIÉRCOLES': 'mi',
        'MIERCOLES': 'mi',  # Alternativa sin tilde
        'JUEVES': 'j',
        'VIERNES': 'v',
        'SÁBADO': 's',
        'SABADO': 's',  # Alternativa sin tilde
        'DOMINGO': 'd',
    }

    def handle(self, *args, **kwargs):
        # Texto proporcionado (aquí lo puedes sustituir por una entrada dinámica si lo prefieres)
        texto = """
        LUNES
        Gustavo
        Rolando
        Silvia peña
        Mónica rivadero
        Vilma
        Natalia Moyano
        Yésica
        Mecha
        ISA
        Santi
        Alicia
        Noemí
        Marta ipv
        Lalo
        Miriam 40
        Carlos 40
        Fabiana Ludueña
        Laura 40
        Lorena 40
        Daniela 40
        Carolina
        Marcela 40
        Elsa 40
        Miriam IPV
        Mónica escalera
        Escuela René fabarolo

        MARTES
        Turca Lala
        Daniela Garay
        Tania
        Mikeas
        Juana Blas Pascal
        Adriana
        Pocha
        Anderson
        Dolores
        Florentina
        Mariana
        Pastora
        Pamela Polinesia
        Estela Polinesia
        Sabrina Polinesia
        Rosa Polinesia
        Griselda
        ILDA

        MIÉRCOLES
        Horacio
        Dima
        Perla
        Lorena
        Julieta
        Muny Muny
        Mario Loyola
        Carmen
        Laura sol naciente
        Silvia sol
        Chello
        Brenda sol
        Eli sol
        Negó
        Carolina

        JUEVES
        Mónica 2
        Mirta Bazán
        Juana
        Silvia Molina
        Keli
        Adela
        Mónica 1
        Sandra IPV
        Sandra Nadal
        Gustavo

        VIERNES
        Mari jose
        Maria
        Romina
        Anita Pérez
        Nilda
        Lescano
        Ivana
        Santi
        Estela pasaje
        Julieta sol
        Leandra
        Román
        Polleria Lourdes
        Carina Lourdes
        David Lourdes
        Daniela Carranza
        Clarinda
        Patrón Tarde
        Meliza
        Distribuidora
        Estela
        Antonella
        Sole
        Frente sole
        Vero costa canal
        Juan
        Frente colegio
        Karina
        Ariana
        Flor
        Guillermo
        Ceci
        Mariza
        lado mariza
        Rodrigo
        Carlos
        Vero
        Josué
        Víctor
        Suegro
        """

        # Divide el texto en secciones por día
        sections = re.split(r'\n\s*(LUNES|MARTES|MIÉRCOLES|MIERCOLES|JUEVES|VIERNES|SÁBADO|SABADO|DOMINGO)\s*\n', texto, flags=re.IGNORECASE)

        current_day = None
        clients_data = []

        for section in sections:
            section = section.strip()
            if section.upper() in self.DAYS_MAPPING:
                current_day = section.upper()
            elif current_day:
                lines = section.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) == 1:
                            nombre = parts[0]
                            apellido = ''
                        else:
                            nombre = ' '.join(parts[:-1])
                            apellido = parts[-1]
                        codigo_interno = self.DAYS_MAPPING[current_day] + ''.join([p[0].lower() for p in parts])
                        clients_data.append(Cliente(nombre=nombre, apellido=apellido, codigo_interno=codigo_interno))

        # Bulk create clients
        Cliente.objects.bulk_create(clients_data)
        self.stdout.write(self.style.SUCCESS('Clientes cargados exitosamente'))

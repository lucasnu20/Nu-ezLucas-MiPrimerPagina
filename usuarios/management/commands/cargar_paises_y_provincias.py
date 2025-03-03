import os
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from usuarios.models import Pais, Provincia

class Command(BaseCommand):
    help = 'Cargar países y provincias desde un archivo Excel'

    def handle(self, *args, **options):
        # Uso BASE_DIR para construir la ruta al archivo Excel
        archivo_excel = os.path.join(settings.BASE_DIR, 'archivos', 'listado_paises_provincias.xlsx')

        # Cargo el excel en un DataFrame de pandas
        df = pd.read_excel(archivo_excel)

        # Recorro el excel y creo los objetos correspondientes
        for index, row in df.iterrows():
            pais_nombre = row[0]  
            provincia_nombre = row[1]  
            
            
            pais, created = Pais.objects.get_or_create(nombre=pais_nombre)

            # Creo la provincia asociada al país
            Provincia.objects.get_or_create(nombre=provincia_nombre, pais=pais)

        
        self.stdout.write(self.style.SUCCESS("Datos de países y provincias cargados exitosamente."))
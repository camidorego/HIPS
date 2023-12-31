import os
import csv
from datetime import datetime

# funcion para crear un archivo csv en el directorio resultado/
def guardar_resultado_csv(carpeta, nombre_archivo,usuario, cantidad_errores):
    try:
        # se obtiene la fecha actual
        fecha=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # se abre el archivo donde vamos a escribir
        with open(f"/var/log/hips/resultados/{carpeta}/{nombre_archivo}.csv", mode='a', newline='') as file:
            # se inserta la informacion
            writer = csv.writer(file)
            writer.writerow([fecha,usuario, cantidad_errores])
    except Exception as e:
        print(f'Ocurrió un error al guardar los resultados en el archivo CSV: {e}')

# funcion para crear escribir en alarmas,log
def escribir_log(tipo_alarma, mensaje):
    try:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ruta_archivo = os.path.join("/var/log/hips/alarmas.log")
        with open(ruta_archivo, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fecha, tipo_alarma, mensaje])
    except Exception as e:
        print(f'Ocurrió un error al guardar los resultados en alarmas.log: {e}')

# funcion para escribir en prevencion.log
def escribir_prevencion(mensaje):
    try:
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ruta_archivo = os.path.join("/var/log/hips/prevencion.log")
        with open(ruta_archivo, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([mensaje])
    except Exception as e:
        print(f'Ocurrió un error al guardar los resultados en prevencion.log: {e}')
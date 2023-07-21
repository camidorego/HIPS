import csv
from datetime import datetime


def guardar_resultado_csv(carpeta, nombre_archivo,usuario, cantidad_errores):
    try:
        fecha=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("/var/log/hips/{carpeta}/{nombre_archivo}.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fecha, usuario, cantidad_errores])
        print("Los resultados han sido guardados en resultados.csv")
    except Exception as e:
        print(f'Ocurrió un error al guardar los resultados en el archivo CSV: {e}')
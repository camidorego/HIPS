import subprocess
import csv
from datetime import datetime

try:
    fecha=datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # se obtienen los usuarios conectados y sus respectivos puertos. Se convierte todo a texto con decode
    salida_texto = subprocess.check_output("who -H | awk '{print $1, $5}'", shell=True).decode('utf-8')

    # se saca 'NAMES' y se convierte a un array
    salida_array = salida_texto.splitlines()[1:]

    print("Los usuarios conectados son: ",salida_array)

    # Creamos una lista con tuplas (nombre_usuario, direccion_ip)
    usuarios_ip = [tuple(linea.strip().split()) for linea in salida_array]

    # Guardamos la informacion en un archivo CSV
    with open('/var/log/hips/usuarios_conectados.csv', 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["FECHA Y HORA", "NOMBRE", "IP"])
        for usuario in usuarios_ip:
            print(fecha, usuario)
            writer.writerow([fecha, usuario])
    

except:
    print('Ocurrio un error')


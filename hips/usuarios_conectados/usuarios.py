import subprocess
import os
import sys
# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)

import escribir_resultado


try:
    
    # se obtienen los usuarios conectados y sus respectivos puertos. Se convierte todo a texto con decode
    salida_texto = subprocess.check_output("who -H | awk '{print $1, $5}'", shell=True).decode('utf-8')

    # se saca 'NAMES' y se convierte a un array
    salida_array = salida_texto.splitlines()[1:]

    print("Los usuarios conectados son: ",salida_array)

    # Creamos una lista con tuplas (nombre_usuario, direccion_ip)
    usuarios_ip = [tuple(linea.strip().split()) for linea in salida_array]

    # se guarda en un csv
    for usuario,ip in usuarios_ip:
        escribir_resultado.guardar_resultado_csv('usuarios_conectados','usuarios',usuario,ip)

except:
    print('Ocurrio un error')


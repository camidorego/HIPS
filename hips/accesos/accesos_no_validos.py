import re
import os
import sys
import subprocess

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)

import hips.escribir_resultado as escribir_resultado

def buscar_acceso_indebido():
    try:
        resultado = subprocess.run("sudo cat /var/log/secure | grep -i 'sshd' | grep -i 'Failed password'", shell=True, capture_output=True, text=True).stdout.split('\n')[:-1]
    except:
        print("Error al buscar accesos indebidos")

    contador_ip = {}

    for line in resultado:
        ip_origen = line.split()[-4] 
        if ip_origen in contador_ip:
            contador_ip[ip_origen]= contador_ip[ip_origen] + 1
        else:
            contador_ip[ip_origen]=1
    
    for ip, count in contador_ip:
        if count > 8:
            escribir_resultado.guardar_resultado_csv('accesos','accesos_no_validos',f'Se encontraron {count} intentos de acceso',f'desde {ip}')
            escribir_resultado.escribir_log('Acceso Indebido', f'Se encontraron {count} intentos de acceso desde {ip}')
               

if __name__ == "__main__":
    buscar_acceso_indebido()

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

import escribir_resultado

# directorio controlar_logs
logs_dir = os.path.join(parent_dir, 'controlar_logs')
sys.path.append(logs_dir)

import acciones

def buscar_acceso_indebido():
    # se ejecuta el comando para analizar el log. Buscamos todas las lineas que tengan 'Failed password'
    try:
        resultado = subprocess.run("sudo cat /var/log/secure | grep -i 'sshd' | grep -i 'Failed password'", shell=True, capture_output=True, text=True).stdout.split('\n')[:-1]
    except:
        print("Error al buscar accesos indebidos")

    contador_ip = {}
    # se ve desde que IP se intenta conectar y cuantas veces
    for line in resultado:
        ip_origen = line.split()[-4] 
        if ip_origen in contador_ip:
            contador_ip[ip_origen]= contador_ip[ip_origen] + 1
        else:
            contador_ip[ip_origen]=1
    
    # si es mayor a 8 veces se genera la alarma y se le informa al administrador
    for ip, count in contador_ip:
        if count > 8:
            escribir_resultado.guardar_resultado_csv('accesos','accesos_no_validos',f'Se encontraron {count} intentos de acceso',f'desde {ip}')
            escribir_resultado.escribir_log('Acceso Indebido', f'Se encontraron {count} intentos de acceso desde {ip}')
            acciones.enviar_mail('Alarma!','Acceso Indebido',f'Se encontraron {count} intentos de acceso desde {ip}')
               

if __name__ == "__main__":
    buscar_acceso_indebido()

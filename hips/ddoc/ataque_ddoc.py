import subprocess
import os
import sys

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# directorio controlar_logs
logs_dir = os.path.join(parent_dir, 'controlar_logs')

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)
sys.path.append(logs_dir)
print(logs_dir,parent_dir)

import escribir_resultado
import acciones

def buscar_ddoc():
    resultado = subprocess.check_output("sudo grep -i 'IP' /var/log/ddoc/info.log | awk '{print $3, $5}'", shell=True).decode('utf-8')

    ips = {}  # Usamos un diccionario para almacenar las ocurrencias de los pares de IP
    lines = resultado.strip().split('\n')
    for line in lines:
        ip_origen, ip_destino = line.split()
        if (ip_origen, ip_destino) in ips:
            ips[(ip_origen, ip_destino)] += 1
        else:
            ips[(ip_origen, ip_destino)] = 1
    
    for ip_pair, occurrences in ips.items():
        if occurrences > 10:
            print(f"La IP {ip_pair[0]} intento conectarse a {ip_pair[1]} {occurrences} veces. Esto puede indicar un ataque DDoC")
            escribir_resultado.guardar_resultado_csv('ddoc','ataque_ddoc',f'La IP {ip_pair[0]} intento conectarse a {ip_pair[1]}',f'{occurrences} veces. Esto puede indicar un ataque DDoC, se bloqueara la IP {ip_pair[0]} por seguridad')
            escribir_resultado.escribir_log('Denegación de Servicio (DDoC)',f'La IP {ip_pair[0]} intento conectarse a {ip_pair[1]} {occurrences} veces. Esto puede indicar un ataque DDoC')
            print(f'Se bloqueara la IP {ip_pair[0]} por seguridad')
            escribir_resultado.escribir_prevencion(f'Se bloqueara la IP {ip_pair[0]} por seguridad')
            acciones.bloquear_ip({ip_pair[0]})
    
    

if __name__=="__main__":
    buscar_ddoc()
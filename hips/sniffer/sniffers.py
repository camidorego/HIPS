import subprocess
import os
import sys

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)

# directorio controlar_logs
logs_dir = os.path.join(parent_dir, 'controlar_logs')

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)
sys.path.append(logs_dir)

import escribir_resultado
import acciones

def detectar_sniffers():
    sniffers_conocidos = ["tcpdump", "tshark", "wireshark"]
    sniffers_en_ejecucion = []
    
    # Se ejecuta el comando para ver si alguno de los programas se está ejecutando
    for sniffer in sniffers_conocidos:
        comando = f"ps -aux | grep {sniffer} | grep -v grep | awk '{{print $1, $2}}'"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        # Si se encontró un programa en ejecución, se guarda la información en el csv y se genera la alarma
        if resultado.stdout.strip():
            lines = resultado.stdout.strip().split("\n")
            for line in lines:
                usuario, pid = line.split()
            if usuario != "root":
                print(f"Se ha detectado el proceso {sniffer} en ejecución por otro usuario que no es root. Esto podría indicar la presencia de un sniffer.")
                escribir_resultado.guardar_resultado_csv('sniffer', 'sniffers', f"Se detectó el proceso en ejecución {sniffer} por un usuario que no es root. Puede indicar la presencia de un sniffer. Por seguridad, se terminara el proceso", resultado.stdout)
                escribir_resultado.escribir_log('Posible sniffer', f"Se ha detectado el proceso {sniffer} en ejecución. Esto podría indicar la presencia de un sniffer.")
                sniffers_en_ejecucion.append(sniffer)
                subprocess.run(f"kill -9 {pid}", shell=True)
                print(f"El proceso {sniffer} con PID {pid} ha sido terminado.")
                escribir_resultado.escribir_prevencion(f"Se termino el proceso {pid}, {sniffer} porque estaba siendo ejecutado por un usuario no autorizado")
            else:
                print(f"El proceso {sniffer} con PID {pid} está siendo ejecutado por el usuario root. No se terminará.")
        # Si no se encontró ningún programa corriendo, también se guarda el resultado en un csv
        else:
            print(f"No se encontró ningun proceso '{sniffer}'. El sistema es seguro.")
            escribir_resultado.guardar_resultado_csv('sniffer', 'sniffers', f"No se encontró ningun proceso '{sniffer}'. El sistema es seguro.", '')
    
    # Se envía un correo al administrador si se encontraron sniffers en ejecución
    if len(sniffers_en_ejecucion) != 0:
        acciones.enviar_mail('Alarma!', 'Posible sniffer', f"Se encontraron los siguientes procesos en ejecución: {', '.join(sniffers_en_ejecucion)}")
        
def modo_promiscuo(): 
    # Se ejecuta el código para saber si el sistema entró en modo promiscuo
    resultado = os.popen("sudo ip a show enp0s3 | grep -i promisc").read()
    
    # Se analiza el resultado y se guarda en el csv y se genera la alarma
    if resultado.strip():  # Verificamos si la cadena no está vacía
        print(resultado)
        print('Puede que el sistema haya entrado en modo promiscuo según los resultados. Por seguridad, sera desactivado')
        escribir_resultado.guardar_resultado_csv('sniffer', 'sniffers', f'Puede que el sistema haya entrado en modo promiscuo según los resultados {resultado}', ". Por seguridad, sera desactivado")
        escribir_resultado.escribir_log('Posible sniffer', f'Puede que el sistema haya entrado en modo promiscuo según los resultados: {resultado}')
        
        # Se envía un correo al administrador
        acciones.enviar_mail('Posible sniffer', 'Sistema en modo promiscuo', f'Puede que el sistema haya entrado en modo promiscuo según los resultados: {resultado}')

        # Ejecutamos el comando para que el sistema no esté en modo promiscuo
        subprocess.run("sudo ip link set enp0s3 promisc off", shell=True)
        escribir_resultado.guardar_resultado_csv('sniffer', 'sniffers', 'El modo promiscuo fue desactivado', "")
        escribir_resultado.escribir_prevencion("El sistema estaba en modo promiscuo, pero ya se desactivo.")
    else:
        print(resultado)
        print("Todo bien")
        escribir_resultado.guardar_resultado_csv('sniffer', 'sniffers', 'El sistema es seguro, no entró en modo promiscuo', '')

if __name__ == "__main__":
    detectar_sniffers()
    modo_promiscuo()

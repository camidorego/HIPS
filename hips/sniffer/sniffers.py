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
    sniffers=[]
    
    for sniffer in sniffers_conocidos:
        comando = f"ps -aux | grep {sniffer} | grep -v grep |  awk '{{print $1, $2, $NF}}'"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(resultado)

        if resultado.returncode != 0:
            print(f'Se ha detectado el proceso {sniffer} en ejecución. Esto podría indicar la presencia de un sniffer.')
            escribir_resultado.guardar_resultado_csv('sniffer','sniffers',f'Se detecto el proceso en ejecucion {sniffer}','. Puede indicar la presencia de un sniffer')
            escribir_resultado.escribir_log('Posible sniffer',f"Se ha detectado el proceso {sniffer} en ejecución. Esto podría indicar la presencia de un sniffer.")
            sniffer.append(sniffer)

        else:
            print(f"No se encontro ningun proceso '{sniffer}'. El sistema es seguro")
            escribir_resultado.guardar_resultado_csv('sniffer','sniffers',f"No se encontro ningun proceso '{sniffer}'. El sistema es seguro",'')
            
    # se envia un correo al administrador
    if len(sniffers)!=0:
        acciones.enviar_mail('Alarma!','Posible sniffer', f'Se encontraron los siguientes procesos en ejecucion: {sniffers}')



def modo_promiscuo(): 
    resultado = os.popen("sudo ip a show enp0s3 | grep -i promis").read()
    if resultado!='':
        print(resultado)
        print('Puede que el sistema haya entrado en modo promiscuo segun los resultados')
        escribir_resultado.guardar_resultado_csv('sniffer','sniffers','Puede que el sistema haya entrado en modo promiscuo segun los resultados',resultado)
        escribir_resultado.escribir_log('Posible sniffer',f'Puede que el sistema haya entrado en modo promiscuo segun los resultados: {resultado}')
        acciones.enviar_mail('Posible sniffer', 'Sistema en modo promiscup',f'Puede que el sistema haya entrado en modo promiscuo segun los resultados: {resultado}')
    else:
        print(resultado)
        print("Todo bien")
        escribir_resultado.guardar_resultado_csv('sniffer','sniffers','El sistema es seguro, no entro en modo promiscuo','')

if __name__ == "__main__":
    detectar_sniffers()
    modo_promiscuo()

import subprocess
import os
import sys
import csv
# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)

# directorio controlar_logs
logs_dir = os.path.join(parent_dir, 'controlar_logs')

sys.path.append(logs_dir)

import escribir_resultado
import revisar_logs

def tamanho_cola():
    try:
        # Ejecuta el comando "mailq" para ver el tamanho de la cola
        output = subprocess.check_output(['mailq'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        # Si hay un error al ejecutar "mailq", muestra un mensaje de error
        print(f"Error al ejecutar el comando 'mailq': {e}")
        return None

    # Procesa la salida para obtener el tamaño de la cola de correos
    lines = output.strip().split('\n')
    cola = len(lines) - 1  # Restamos 1 para excluir la primera línea que muestra el número de mensajes
    return cola

def main():
    cola = tamanho_cola()
    if cola is not None:
        # se muestra el tamanho de la cola y se guarda en un csv
        print(f"Tamaño de la cola de correos: {cola} mensajes.")
        escribir_resultado.guardar_resultado_csv('ver_cola_mail','ver_cola_mail','tamanho de cola de mail',cola)
        
        # si la cola es muy grande se revisa si hay envios masivos a un mismo destinatario y se bloquea
        if cola>50:
            escribir_resultado.escribir_log('Cola de Correo',f'tamanho masivo de cola de mail {cola}')
            revisar_logs.buscar_mails_masivos()
            

if __name__ == "__main__":
    main()

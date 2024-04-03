import psutil
import time
import sys
import os
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

def kill_process(process_info):
    # terminamos el proceso
    try:
        pid = process_info['pid']
        process = psutil.Process(pid)
        process.terminate()
        print(f"Proceso {process_info['name']} (PID: {pid}) terminado.")
    except psutil.NoSuchProcess:
        print(f"Proceso {process_info['name']} (PID: {pid}) no encontrado.")

def revisar_procesos():
    procesos_terminados = []

    try:
        for process in psutil.process_iter(['pid', 'name', 'memory_percent', 'create_time']):
            # guardamos la informacion relevante de los procesos
            process_name = process.info['name']
            process_pid = process.info['pid']
            memory_percent = process.info['memory_percent']
            create_time = process.info['create_time']
            
            if process_name in ('systemd', 'gnome-s+', 'gnome-shell','bash', 'chrome','python3','flask'):
                # Ignorar los procesos del sistema
                continue

            if memory_percent > 10.0:
                elapsed_time_seconds = time.time() - create_time

                print(f"Proceso: {process_name} (PID: {process_pid})")
                print(f"  Uso de Memoria: {memory_percent:.2f}%")
                print(f"  Tiempo de ejecución: {elapsed_time_seconds:.2f} segundos")
                print("-" * 30)

                # Guardar la información en los logs
                escribir_resultado.guardar_resultado_csv('procesos', 'revisar_procesos', f" - PID: {process_pid}, Nombre: {process_name}, Uso de memoria: {memory_percent:.2f}%, Tiempo: {elapsed_time_seconds:.2f} segundos", '')
                escribir_resultado.escribir_log('Proceso consumiendo mucha memoria', f" - PID: {process_pid}, Nombre: {process_name}, Uso de memoria: {memory_percent:.2f}%, Tiempo: {elapsed_time_seconds:.2f} segundos")

                if elapsed_time_seconds > 10:
                    # Terminamos el proceso con la funcion kill_process
                    kill_process(process.info)
                    escribir_resultado.guardar_resultado_csv('procesos', 'revisar_procesos', f"Se terminó el proceso {process_name} porque consumía el {memory_percent:.2f}% de memoria por {elapsed_time_seconds:.2f} segundos", '')
                    procesos_terminados.append(process_name)
                    escribir_resultado.escribir_prevencion(f"Se terminó el proceso por alto consumo de memoria -> PID: {process_pid}, Nombre: {process_name}, Uso de memoria: {memory_percent:.2f}%, Tiempo: {elapsed_time_seconds:.2f} segundos")

        if procesos_terminados:
            # se le informa al administrador
            acciones.enviar_mail('Alarma!', 'Rendimiento del sistema', f'Se terminaron los procesos {", ".join(procesos_terminados)} porque consumían demasiada memoria')
        else:
            escribir_resultado.guardar_resultado_csv('procesos', 'revisar_procesos', 'No se encontraron procesos que consumen mucha memoria', '')

    except psutil.Error as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    revisar_procesos()


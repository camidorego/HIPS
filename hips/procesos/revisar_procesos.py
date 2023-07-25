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

def procesos_mucha_memoria(memory_threshold_mb, time_threshold_seconds):
    high_memory_processes = []
    # cada proceso en ejecucion se revisa cuanto de memoria consume
    for process in psutil.process_iter(['pid', 'name', 'memory_percent', 'create_time']):
        # de acuerdo a lo que se paso como parametro de lo que se considera un uso excesivo de memoria
        if process.info['memory_percent'] > memory_threshold_mb:
            elapsed_time_seconds = time.time() - process.info['create_time']
            if elapsed_time_seconds >= time_threshold_seconds:
                high_memory_processes.append(process.info)

    return high_memory_processes

def kill_processes(process_list):
    # se terminan los procesos que se pasaron como parametro
    for process_info in process_list:
        try:
            pid = process_info['pid']
            process = psutil.Process(pid)
            process.terminate()
            print(f"Proceso {process_info['name']} (PID: {pid}) terminado.")
        except psutil.NoSuchProcess:
            print(f"Proceso {process_info['name']} (PID: {pid}) no encontrado.")

def main():
    memory_threshold_mb = 20  # Porcentaje de memoria a partir del cual se considera elevado
    time_threshold_seconds = 300  # Tiempo en segundos a partir del cual se considera consumo excesivo

    high_memory_processes = procesos_mucha_memoria(memory_threshold_mb, time_threshold_seconds)
    # se analiza el resultado y se escribe en el csv
    if not high_memory_processes:
        print("No se encontraron procesos con consumo elevado de memoria.")
        escribir_resultado.guardar_resultado_csv('procesos','revisar_procesos',"No se encontraron procesos con consumo elevado de memoria.",'')
    else:
        print("Procesos con consumo elevado de memoria:")
        
        for process_info in high_memory_processes:
            print(f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")
            escribir_resultado.guardar_resultado_csv('procesos','revisar_procesos',f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%",'')
            escribir_resultado.escribir_log('Proceso consumiendo mucha memoria',f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")
        # se terminan los procesos que consumen mucha energia
        kill_processes(high_memory_processes)
        # se informan sobre los procesos terminados
        escribir_resultado.escribir_prevencion(f"Se termino el proceso por alto consumo de memoria -> PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")
        # se le manda un mail al administrador
        acciones.enviar_mail('Alarma!','Rendimiento del sistema', f'Se terminaron los procesos {high_memory_processes} porque consumian demasiada memoria')

        

if __name__ == "__main__":
    main()

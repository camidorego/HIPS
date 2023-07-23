import psutil
import time
import escribir_csv

def procesos_mucha_memoria(memory_threshold_mb, time_threshold_seconds):
    high_memory_processes = []

    for process in psutil.process_iter(['pid', 'name', 'memory_percent', 'create_time']):
        if process.info['memory_percent'] > memory_threshold_mb:
            elapsed_time_seconds = time.time() - process.info['create_time']
            if elapsed_time_seconds >= time_threshold_seconds:
                high_memory_processes.append(process.info)

    return high_memory_processes

def kill_processes(process_list):
    for process_info in process_list:
        try:
            pid = process_info['pid']
            process = psutil.Process(pid)
            process.terminate()
            print(f"Proceso {process_info['name']} (PID: {pid}) terminado.")
        except psutil.NoSuchProcess:
            print(f"Proceso {process_info['name']} (PID: {pid}) no encontrado.")

def main():
    memory_threshold_mb = 10  # Porcentaje de memoria a partir del cual se considera elevado
    time_threshold_seconds = 300  # Tiempo en segundos a partir del cual se considera consumo excesivo

    high_memory_processes = procesos_mucha_memoria(memory_threshold_mb, time_threshold_seconds)

    if not high_memory_processes:
        print("No se encontraron procesos con consumo elevado de memoria.")
    else:
        print("Procesos con consumo elevado de memoria:")
        for process_info in high_memory_processes:
            print(f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")
            escribir_csv.guardar_resultado_csv('verificar_procesos','procesos_alto_consumo',process_info,'')

        # Pregunta si desea matar los procesos identificados
        response = input("¿Desea matar los procesos identificados? [y/N]: ").lower()
        if response == 'y':
            kill_processes(high_memory_processes)
        else:
            print("Los procesos no fueron terminados.")

if __name__ == "__main__":
    main()

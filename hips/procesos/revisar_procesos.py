import psutil
import time
import hips.escribir_resultado as escribir_resultado

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
            escribir_resultado.guardar_resultado_csv('procesos','revisar_procesos',f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%",'')
            escribir_resultado.escribir_log('Proceso consumiendo mucha memoria',f" - PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")

        kill_processes(high_memory_processes)
        escribir_resultado.escribir_prevencion(f"Se termino el proceso por alto consumo de memoria -> PID: {process_info['pid']}, Nombre: {process_info['name']}, Uso de memoria: {process_info['memory_percent']}%")

        

if __name__ == "__main__":
    main()

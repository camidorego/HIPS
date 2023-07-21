import subprocess
import revisar_logs

def tamanho_cola():
    try:
        # Ejecuta el comando "mailq" y obtiene la salida
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
        print(f"Tamaño de la cola de correos: {cola} mensajes.")
        # si la cola es muy grande se revisa si hay envios masivos a un mismo destinatario y se bloquea
        if cola>50:
            revisar_logs.buscar_mails_masivos()

if __name__ == "__main__":
    main()

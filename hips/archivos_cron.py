import subprocess
import escribir_csv

def lista_usuarios():
    # obtenemos la lista de usuarios
    with open('/etc/passwd') as lista_usuarios:
        return [line.split(':')[0] for line in lista_usuarios]

def verificar_cron():
    users = lista_usuarios()
    
    archivos_cron = []
    
    for user in users:
        try:
            # para cada usuario ejecutamos el comando sudo crontab -l -u nombre_usuario
            resultado = subprocess.check_output(['sudo', 'crontab', '-l', '-u', user], stderr=subprocess.STDOUT, text=True)
            if resultado.strip():
                archivos_cron.append((user, resultado.strip()))
        except subprocess.CalledProcessError:
            # si el usuario no tiene cron o no se puede acceder a su cron, omitimos el usuario.
            pass
    
    return archivos_cron

def main():
    archivos_cron = verificar_cron()
    
    if not archivos_cron:
        print("No se encontraron archivos de cron para ningún usuario en el sistema.")
    else:
        print("Archivos de cron encontrados para los siguientes usuarios:")
        for user, cron_archivo in archivos_cron:
            print(f"Usuario: {user}")
            print(cron_archivo, '\n')

            # se guarda la informacion en el csv
            escribir_csv.guardar_resultado_csv('verificar_procesos','archivos_cron',user,cron_archivo)
            
        print("Se le notificara al administrador")
        #enviar correo al administrador

        
            

if __name__ == "__main__":
    main()

import subprocess
import sys
import os

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)
import escribir_resultado

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
        escribir_resultado.guardar_resultado_csv('cron','archivos_cron','No se encontraron archivos de cron para ningún usuario en el sistema.','')
    else:
        print("Archivos de cron encontrados para los siguientes usuarios:")
        for user, cron_archivo in archivos_cron:
            print(f"Usuario: {user}")
            print(cron_archivo, '\n')

            # se guarda la informacion en el csv
            escribir_resultado.guardar_resultado_csv('cron','archivos_cron',user,cron_archivo)
            escribir_resultado.escribir_log('Cron', f'Se encontro el archivo de cron {cron_archivo} ejecutandose para el usuario {user}')
            
        print("Se le notificara al administrador")
        escribir_resultado.escribir_prevencion(f'Se envio un correo al administrador porque se encontro el archivo de cron {cron_archivo} ejecutandose para el usuario {user}')
        #enviar correo al administrador

        
            

if __name__ == "__main__":
    main()

import subprocess
from collections import Counter
import re
import acciones
import os
import sys

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)
import escribir_resultado


def buscar_error_autentificacion():
    try:
        #output = subprocess.check_output(["sudo","grep", "authentication failure", "/var/log/secure"]).decode('utf-8')
        #output=subprocess.run(["sudo","grep", "authentication failure", "/var/log/secure"], check=True, capture_output=True).stdout.decode('utf-8').strip()
        output=subprocess.check_output("sudo cat /var/log/httpd/access.log | grep -i 'HTTP' | grep -i '404'", shell=True).decode('utf-8')
        if output:
            usuarios_errores = re.findall(r'user=(\S+)', output)
            contador_errores = Counter(usuarios_errores)

            print("Se encontraron intentos de inicio de sesión fallidos:")

            for usuario, cantidad_errores in contador_errores.items():
                # se guarda en el csv
                escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',usuario, cantidad_errores)
                escribir_resultado.escribir_log('Autenticación Fallida',f'Se encontraron {cantidad_errores} errores de autenticacion para {usuario}')

                if cantidad_errores > 10: # si hubieron mas de 10 intentos fallidos de inicio de sesion, se cambia la contrasena de usuario
                    print(f"El usuario {usuario} tuvo {cantidad_errores} errores de autenticación. Por seguridad, se bloqueara al usuario")
                    escribir_resultado.escribir_prevencion(f'Se bloqueo al usuario {usuario} porque se encontraron {cantidad_errores} errores de autenticacion')
                          
                    # se bloquea al usuario temporalmente
                    acciones.bloquear_usuario(usuario)

        else:
            print("No se encontraron intentos de inicio de sesión fallidos o no hubo más de 5 errores para ningún usuario.")

    except Exception as e:
        print(f'Ocurrió un error al buscar errores de autenticación: {e}')

def buscar_failed_password_secure():
    try:
        #output = subprocess.check_output(["sudo","grep", "password check failed", "/var/log/secure"]).decode('utf-8')
        output=subprocess.run(["sudo","grep", "password check failed", "/var/log/secure"], check=True, capture_output=True).stdout.decode('utf-8').strip()
        if output:
            usuarios_errores = re.findall(r'user (\S+)', output)
            contador_errores = Counter(usuarios_errores)
            print("Se encontraron intentos de inicio de sesión fallidos:")
            for usuario, cantidad_errores in contador_errores.items():
                # se guarda en el csv
                escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',usuario, cantidad_errores)
                escribir_resultado.escribir_log('Password Check Failed',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}')

                if cantidad_errores > 10: # si hubieron mas de 10 intentos fallidos de inicio de sesion, se cambia la contrasena de usuario
                    print(f"El usuario {usuario} tuvo {cantidad_errores} errores de autenticación. Se cambiara la contrasena del usuario por seguridad")

                    # se cambia la contrasena del usuario
                    nueva_contrasena=input(f"Ingresa una contrasenha temporal para el usuario: {usuario}")
                    escribir_resultado.escribir_prevencion(f'Se cambio la contrasenha del usuario {usuario} porque se encontraron {cantidad_errores} intentos de inicio de sesión fallidas')
                    acciones.cambiar_contrasena(usuario, nueva_contrasena)

                    
        else:
            print("No se encontraron intentos de inicio de sesión fallidos o no hubo más de 5 errores para ningún usuario.")
    except:
        print('Ocurrio un error al buscar errores de contrasenas')

def buscar_authentication_failure_messages():
    try:
        resultado = subprocess.check_output("sudo grep -i 'service=smtp' /var/log/messages | grep -i 'auth failure'", shell=True).decode('utf-8')
        
        
        if resultado.stdout:
            print("Se encontraron eventos de autenticación fallida:")
            print(resultado.stdout)
            # Implementar acciones de respuesta según sea necesario
    except:
        print('Ocurrio un error al buscar errores de autenticacion')

def buscar_errores_httpd():
    try:
        resultado = subprocess.check_output("sudo grep -i 'HTTP' /var/log/httpd/access_log | grep -i '404' | awk '{print $1, $9}'", shell=True).decode('utf-8')
        print(resultado)
        ips=[]
        for linea in resultado.splitlines():
            ip=linea.split()[0] # juntamos todas las direcciones ip
            ips.append(ip)
        contador_ip=Counter(ips)
        for ip, cantidad_errores in contador_ip.items():
            # se guarda en el csv
            escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',ip, cantidad_errores)
            escribir_resultado.escribir_log('Anomalias de Trafico', f"La IP {ip} ha generado {cantidad_errores} errores 404 en el registro de acceso.")
            if cantidad_errores > 10:
                print(f"La IP {ip} ha generado {cantidad_errores} errores 404 en el registro de acceso.")

                # bloqueamos la ip 
                acciones.bloquear_ip(ip)
                escribir_resultado.escribir_prevencion(f'Por seguridad se bloqueo la ip {ip} porque ha generado {cantidad_errores} errores 404 en el registro de acceso.')
    except:
        print('Ocurrio un error al buscar errores de cargas de paginas web ')

def buscar_mails_masivos():
    with open('/var/log/maillog', 'r') as maillog_file:
        maillog = maillog_file.readlines()

    # Expresión regular para buscar las direcciones de correo electrónico y verificamos que el status sea enviado o en camino

    #email_pattern = re.compile(r'to=<([\w\.-]+@[\w\.-]+)>')
    email_reggex= re.compile(r'to=<([\w\.-]+@[\w\.-]+)>.* status=(sent|delivered|queued)')

    # Diccionario para almacenar la cantidad de envíos a cada dirección
    envios_por_direccion = Counter()

    for linea in maillog:
        # Buscar las direcciones de correo electrónico en cada línea
        direcciones = email_reggex.findall(linea)
        for direccion in direcciones:
            # Incrementar el contador para cada dirección encontrada
            envios_por_direccion[direccion] += 1

    # Filtrar las direcciones con más de cierta cantidad de envíos (por ejemplo, más de 10 envíos)
    envios_masivos = {direccion: cantidad for direccion, cantidad in envios_por_direccion.items() if cantidad > 2}

    for direccion, cantidad in envios_masivos.items():
        # se guarda en el csv
        escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',direccion, cantidad)
        escribir_resultado.escribir_log('Seguridad de Correo Electrónico',f"A la dirección {direccion} se le envio {cantidad} correos")
        print(f"Dirección: {direccion}, Cantidad de envíos: {cantidad}")
        if cantidad>50:
            #Bloqueamos el correo
            acciones.bloquear_email(direccion)
            escribir_resultado.escribir_prevencion(f'Se bloque la direccion {direccion} por envio de correos masivos')


def main():
    #print("Iniciando programa de detección y respuesta de seguridad...")
    buscar_failed_password_secure()
    buscar_authentication_failure_messages()
    buscar_errores_httpd()
    buscar_mails_masivos()

if __name__ == "__main__":
    main()

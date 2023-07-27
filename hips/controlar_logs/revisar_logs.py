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


def buscar_access_log():
    try:
        output = subprocess.check_output("sudo cat /var/log/httpd/access.log | grep -i 'HTTP' | grep -i '404'", shell=True).decode('utf-8')
        if output:
            ips_ocurrencias = {}  # Creamos un diccionario vacío para almacenar las ocurrencias de cada IP
            lines = output.split('\n')
            for line in lines:
                if line:
                    ip = line.split(' ')[0]
                    # Verificamos si la IP ya está en el diccionario, si no, la agregamos con ocurrencia 1, si sí, incrementamos su ocurrencia
                    if ip in ips_ocurrencias:
                        ips_ocurrencias[ip] += 1
                    else:
                        ips_ocurrencias[ip] = 1

            for ip,cantidad_errores in ips_ocurrencias.items():
                escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',f'En access_log se encontro que la IP {ip}', f' tuvo {cantidad_errores} intentos fallidos al conectarse una pagina web')
                escribir_resultado.escribir_log('Autenticación Fallida',f'Se encontraron {cantidad_errores} errores de autenticacion para {ip}')

                if cantidad_errores > 10: # si hubieron mas de 10 intentos fallidos de inicio de sesion, se cambia la contrasena de usuario
                    print(f"La IP {ip} tuvo {cantidad_errores} errores al cargar una pagina. Por seguridad, se bloqueara la IP")
                    escribir_resultado.escribir_prevencion(f'Se bloqueo a la IP {ip} porque se encontraron {cantidad_errores} intentos fallidos para conectarse a una pagina')
                    acciones.enviar_mail('Autenticación Fallida', 'Demasiados intentos fallidos para conectarse a una pagina',f'Se encontraron {cantidad_errores} errores de autenticacion para {ip}. Por seguridad se bloqueo a la IP {ip}')
                          
                    # se bloquea al usuario temporalmente
                    acciones.bloquear_ip(ip)
        else:
            print('no se encontraron errores de acceso')
            escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs','no se encontraron errores de acceso', '')
    except Exception as e:
        print(f'Ocurrio un error al buscar errores de cargas de paginas web: {e}')

def buscar_mail_log():
    email_count = {}
    try:
        result = subprocess.run(['sudo', 'cat', '/var/log/maillog.log'], capture_output=True, text=True, check=True)
        output = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error al leer el archivo: {e}")
        return email_count

    # Procesar el contenido del archivo para contar los correos enviados desde cada dirección
    for line in output:
        if 'from=<' in line and 'to=' in line:
            email_from = line.split('from=<')[1].split('>')[0]
            email_count[email_from] = email_count.get(email_from, 0) + 1

    for direccion, cantidad in email_count.items():
        # se guarda en el csv
        escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',f'La direccion de correo {direccion} envio', f' {cantidad} correos')
        escribir_resultado.escribir_log('Seguridad de Correo Electrónico',f"La dirección {direccion} le envio {cantidad} correos")
        print(f"Dirección: {direccion}, Cantidad de envíos: {cantidad}")
        if cantidad>50:
            #Bloqueamos el correo
            acciones.bloquear_email(direccion)
            escribir_resultado.escribir_prevencion(f'Se bloque la direccion {direccion} por envio de correos masivos')
            acciones.enviar_mail('Seguridad de Correo Electrónico', 'envio masivo de correos',f"La dirección {direccion} le envio {cantidad} correos. Por seguridad se bloque la direccion {direccion}")

def buscar_secure_log():
    try:
        result = subprocess.run("sudo cat /var/log/secure.log | grep -i 'pam_unix(smtp:auth): authentication failure'", shell=True, capture_output=True, text=True, check=True)
        
        if result:
            lines = result.stdout.splitlines()
            user_ocurrencias = {}  # Creamos un diccionario vacío para almacenar las ocurrencias de cada usuario
            for line in lines:
                if 'ruser=' in line and 'user=' in line:
                    semi_line = line.split('ruser=')[1]
                    if 'user=' in semi_line:
                        user = semi_line.split('user=')[1].split()[0]
                        user_ocurrencias[user] = user_ocurrencias.get(user, 0) + 1

            for usuario, cantidad_errores in user_ocurrencias.items():
                print(f"Se encontraron {cantidad_errores} errores de autenticación para el usuario {usuario}")
                # se guarda en el csv
                escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}','')
                escribir_resultado.escribir_log('Password Check Failed',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}')
                
                if cantidad_errores > 10: # si hubieron mas de 10 intentos fallidos de inicio de sesion, se cambia la contrasena de usuario
                    print(f"El usuario {usuario} tuvo {cantidad_errores} errores de autenticación. Se cambiara la contrasena del usuario por seguridad")

                    # se cambia la contrasena del usuario
                    nueva_contrasena=acciones.cambiar_contrasena(usuario)
                    escribir_resultado.escribir_prevencion(f'Se cambio la contrasenha del usuario {usuario} a {nueva_contrasena} porque se encontraron {cantidad_errores} intentos de inicio de sesión fallidas')
                    acciones.enviar_mail('Password Check Failed', 'muchos intentos fallidos de inicio de sesion',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}. Se cambio la contrasenha del usuario {usuario} a {nueva_contrasena} por seguridad')
                    
        else:
            print("No se encontraron intentos de inicio de sesión fallidos.")
    except subprocess.CalledProcessError as e:
        print(f"Error al buscar en secure.log: {e}")
    


def buscar_messages_log():
    try:
        result = subprocess.run("cat /var/log/message.log | grep -i 'auth failure' | grep -i 'service=smtp'", shell=True, capture_output=True, text=True, check=True)
        if result:
            lines = result.stdout.splitlines()
            user_ocurrencias = {}  # Creamos un diccionario vacío para almacenar las ocurrencias de cada usuario
            for line in lines:
                if 'user=' in line:
                    user = line.split('user=')[1].split(']')[0]
                    user_ocurrencias[user] = user_ocurrencias.get(user, 0) + 1
            for usuario, cantidad_errores in user_ocurrencias.items():
                print(f"Se encontraron {cantidad_errores} errores de autenticación para el usuario {usuario}")
                # se guarda en el csv
                escribir_resultado.guardar_resultado_csv('controlar_logs', 'revisar_logs',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}','')
                escribir_resultado.escribir_log('Password Check Failed',f'Se encontraron {cantidad_errores} intentos de inicio de sesión fallidas para {usuario}')
                if cantidad_errores > 10: # si hubieron mas de 10 intentos fallidos de inicio de sesion, se cambia la contrasena de usuario
                    print(f"El usuario {usuario} tuvo {cantidad_errores} errores de autenticación. Se cambiara la contrasena del usuario por seguridad")

                    # se cambia la contrasena del usuario
                    nueva_contrasena=acciones.cambiar_contrasena(usuario)
                    escribir_resultado.escribir_prevencion(f'Se cambio la contrasenha del usuario {usuario} a {nueva_contrasena} porque se encontraron {cantidad_errores} intentos de inicio de sesión fallidas')
                    acciones.enviar_mail('Error de Autenticacion', 'Se detectaron muchos intentos fallidos de inicio de sesion',f"Se encontro {cantidad_errores} errores de autenticación para el usuar {usuario}. Se cambio la contrasenha del usuario {usuario} a {nueva_contrasena}, por seguridad")
                    
        else:
            print("No se encontraron intentos de inicio de sesión fallido.")
    except:
        print('Ocurrio un error al buscar errores de autenticacion')


if __name__ == "__main__":
    buscar_access_log()
    buscar_mail_log()
    buscar_secure_log()
    buscar_messages_log()

import subprocess
from collections import Counter
def buscar_mails_masivos():
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
        print(f"Dirección: {direccion}, Cantidad de envíos: {cantidad}")

#buscar_mails_masivos()
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
            
            if cantidad_errores > 10:
                print(f"La IP {ip} ha generado {cantidad_errores} errores 404 en el registro de acceso.")
    except subprocess.CalledProcessError as e:
        print(f"Error al leer el archivo: {e}")
#buscar_errores_httpd()

def buscar_secure_log():
    try:
        command = "sudo cat /var/log/secure.log | grep -i 'pam_unix(smtp:auth): authentication failure'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        
        if result:
            lines = result.stdout.splitlines()
            user_ocurrencias = {}  # Creamos un diccionario vacío para almacenar las ocurrencias de cada usuario
            for line in lines:
                if 'ruser=' in line and 'user=' in line:
                    semi_line = line.split('ruser=')[1]
                    if 'user=' in semi_line:
                        user = semi_line.split('user=')[1].split()[0]
                        user_ocurrencias[user] = user_ocurrencias.get(user, 0) + 1

            for user, ocurrencia in user_ocurrencias.items():
                print(f"Se encontraron {ocurrencia} errores de autenticación para el usuario {user}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")

# Llamamos a la función
#buscar_secure_log()

def buscar_messages_log():
    
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

buscar_messages_log()






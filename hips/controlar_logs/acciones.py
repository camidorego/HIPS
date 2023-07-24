import os
import subprocess

# Agrega a la lista negra de emails recipientes
def bloquear_email(email):
    try:
        comando_para_agregar_en_lista_negra = f"sudo echo '{email} REJECT' >> /etc/postfix/sender_access"
        os.system(comando_para_agregar_en_lista_negra) # Agregamos el email a la lista negra
        
        os.system("sudo postmap hash:/etc/postfix/sender_access") # creamos la base de datos con el comando postmap
    except Exception:
        print("hubo un problema en cargar un email en la lista negra")

def bloquear_ip(ip):
    os.system(f"sudo iptables -I INPUT -s {ip} -j DROP")
    os.system("sudo service iptables save")

def bloquear_usuario(nombre_usuario):
    try:
        # Ejecutar el comando passwd para bloquear el usuario
        proceso = subprocess.Popen(['sudo', 'passwd', '-l', nombre_usuario], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proceso.communicate()

        # Verificar si hubo algún error al bloquear el usuario
        if proceso.returncode == 0:
            print(f"El usuario {nombre_usuario} ha sido bloqueado correctamente.")
        else:
            print(f"Error al bloquear el usuario {nombre_usuario}.")
    except Exception as e:
        print("Error:", e)

def cambiar_contrasena(nombre_usuario, nueva_contrasenha):
    try:
        # Ejecutar el comando passwd para cambiar la contraseña del usuario
        proceso = subprocess.Popen(['sudo', 'passwd', nombre_usuario], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # se escribe la nueva contrasena y se confirma
        proceso.stdin.write(f'{nueva_contrasenha}\n'.encode())
        proceso.stdin.write(f'{nueva_contrasenha}\n'.encode())
        proceso.stdin.flush()

        # se espera a que el comando termine de ejecutarse
        salida, error = proceso.communicate()

        # verificamos si hubo algun error en el cambio de contraseña
        if proceso.returncode == 0:
            print(f"La contrasenha del usuario {nombre_usuario} ha sido cambiada correctamente.")
        else:
            print(f"Error al cambiar la contrasenha del usuario {nombre_usuario}.")
            print("Mensaje de error:", error.decode().strip())

    except Exception as e:
        print("Error:", e)

def enviar_mail(asunto, mensaje):
    print('enviando')

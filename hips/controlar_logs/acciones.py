import os
import subprocess
import random
import string

# Agrega a la lista negra de emails 
def bloquear_email(email):
    try:
        comando_para_agregar_en_lista_negra = f"sudo echo '{email} REJECT' >> /etc/postfix/sender_access"
        os.system(comando_para_agregar_en_lista_negra) # Agregamos el email a la lista negra
        
        os.system("sudo postmap hash:/etc/postfix/sender_access") # creamos la base de datos con el comando postmap
    except Exception:
        print("hubo un problema en cargar un email en la lista negra")

def bloquear_ip(ip):
    os.system(f"sudo iptables -I INPUT -s {ip} -j DROP")
    os.system("sudo systemctl restart iptables")

def desbloquear_ip(ip):
    os.system(f"sudo iptables -D INPUT -s {ip} -j DROP")
    os.system("sudo systemctl restart iptables")

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

def generar_contrasena():
    caracteres_validos = string.ascii_letters + string.digits + string.punctuation
    for i in range(6):
        contrasena = ''.join(random.choice(caracteres_validos))
    return contrasena

def cambiar_contrasena(nombre_usuario):
    nueva_contrasenha=generar_contrasena()
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
            print(f"La contrasenha del usuario {nombre_usuario} ha sido cambiada a {nueva_contrasenha}.")
            return nueva_contrasenha
        else:
            e=error.decode().strip()
            print(f"Error al cambiar la contrasenha del usuario {nombre_usuario}: {e}")
            return None

    except Exception as e:
        print("Error:", e)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import smtplib
import ssl
import configparser

SERVIDOR = "smtp-mail.outlook.com"
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config = configparser.ConfigParser()
config.read(os.path.join(path, 'database.ini'))
HIPS_CORREO_ADMIN = 'camiladoregobarros@gmail.com' #config['ADMIN']['HIPS_CORREO_ADMIN']
HIPS_CORREO = "hips_dorego@outlook.com"
HIPS_CONTRA = "hips2023"
SSL_context = ssl.create_default_context()
port = 587
msg = MIMEMultipart() 

def enviar_mail(alarma, asunto, msje):
    msg['From']= HIPS_CORREO
    msg['To']= HIPS_CORREO_ADMIN
    msg['Subject']= 'Nivel: ' + alarma + ' | '  + 'Asunto: ' + asunto 
    msg.attach(MIMEText(msje, "plain"))
    text = msg.as_string()
    with smtplib.SMTP(SERVIDOR, port) as server:
        server.starttls(context=SSL_context)
        server.login(HIPS_CORREO, HIPS_CONTRA)
        server.sendmail(HIPS_CORREO, HIPS_CORREO_ADMIN, text)
    server.close()


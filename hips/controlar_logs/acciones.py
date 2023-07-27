import os
import subprocess

# Agrega a la lista negra de emails 
def bloquear_email(email):
    try:
        comando_para_agregar_en_lista_negra = f"sudo echo '{email} REJECT' >> /etc/postfix/sender_access"
        os.system(comando_para_agregar_en_lista_negra) # Agregamos el email a la lista negra
        
        os.system("sudo postmap hash:/etc/postfix/sender_access") # creamos la base de datos con el comando postmap
    except Exception:
        print("hubo un problema en cargar un email en la lista negra")

def bloquear_ip(ip):
    try:
        os.system(f"sudo iptables -I INPUT -s {ip} -j DROP")
        os.system("sudo systemctl restart iptables")
        print(f"IP {ip} bloqueada correctamente.")
    except Exception as e:
            print(f"Error al bloquear la IP: {str(e)}")

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

import string
import random

def generar_contrasena():
    caracteres_validos = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choices(caracteres_validos, k=6))
    return contrasena

def cambiar_contrasena(nombre_usuario):
    nueva_contrasenha = generar_contrasena()
    try:
        proceso = subprocess.Popen(['sudo', 'passwd', nombre_usuario], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proceso.stdin.write(f'{nueva_contrasenha}\n'.encode())
        proceso.stdin.write(f'{nueva_contrasenha}\n'.encode())
        proceso.stdin.flush()
        proceso.stdin.close()  # Cierra el stdin del proceso después de interactuar con él.

        salida, error = proceso.communicate()

        if proceso.returncode == 0:
            print(f"La contrasena del usuario {nombre_usuario} ha sido cambiada a {nueva_contrasenha}.")
            return nueva_contrasenha
        else:
            e = error.decode().strip()
            print(f"Error al cambiar la contrasena del usuario {nombre_usuario}: {e}")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return None


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

from dotenv import load_dotenv

load_dotenv()

SERVIDOR = "smtp-mail.outlook.com"
SSL_context = ssl.create_default_context()
port = 587
msg = MIMEMultipart() 

# se obtiene la informacion
EMAIL_HIPS=os.getenv('EMAIL_HIPS')
EMAIL_HIPS_PASSWD=os.getenv('EMAIL_HIPS_PASSWD')
EMAIL_ADMI=os.getenv('EMAIL_ADMI')

# se establece la conexion con el servidor de correo y se manda desde la cuenta de mail del hips
def enviar_mail(alarma, asunto, msje):
    try:
        msg['From']= EMAIL_HIPS
        msg['To']= EMAIL_ADMI
        msg['Subject']= alarma + ' | '  + asunto 
        msg.attach(MIMEText(msje, "plain"))
        text = msg.as_string()
        with smtplib.SMTP(SERVIDOR, port) as server:
            server.starttls(context=SSL_context)
            server.login(EMAIL_HIPS, EMAIL_HIPS_PASSWD)
            server.sendmail(EMAIL_HIPS, EMAIL_ADMI, text)
        server.close()
    except Exception as e:
        print("Error al enviar el correo:", e)


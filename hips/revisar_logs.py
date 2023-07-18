import os
import subprocess

def buscar_error_autentificacion():
    output=subprocess.run(["grep","Failed Password","/var/log/secure"],shell=True)
    if output.stdout:
        print("Se encontraron intentos de inicio de sesion fallidos")

def buscar_failed_password_secure():
    resultado = subprocess.run(["grep", "Failed Password", "/var/log/secure"], capture_output=True, text=True)
    if resultado.stdout:
        print("Se encontraron intentos de inicio de sesión fallidos:")
        print(resultado.stdout)
        # Implementar acciones de respuesta como bloqueo de IP o cambio de contraseña

def buscar_authentication_failure_messages():
    resultado = subprocess.run(["grep", "Authentication Failure", "/var/log/messages"], capture_output=True, text=True)
    if resultado.stdout:
        print("Se encontraron eventos de autenticación fallida:")
        print(resultado.stdout)
        # Implementar acciones de respuesta según sea necesario

def buscar_errores_carga_paginas_httpd():
    resultado = subprocess.run(["awk", '{print $1}', "/var/log/httpd/access.log"], capture_output=True, text=True)
    ips_unicas = set(resultado.stdout.strip().splitlines())
    if len(ips_unicas) > 100:
        print("Se encontraron muchos accesos únicos desde una misma IP, podría ser un escaneo.")
        # Implementar acciones de respuesta como bloqueo de IP o restricción de acceso

def buscar_envio_mails_masivos_maillog():
    resultado = subprocess.run(["grep", "to=<correo_destino>", "/var/log/maillog"], capture_output=True, text=True)
    if resultado.stdout:
        print("Se encontraron eventos de envío de correos masivos:")
        print(resultado.stdout)
        # Implementar acciones de respuesta como bloqueo de cuenta o análisis detallado

def main():
    print("Iniciando programa de detección y respuesta de seguridad...")
    buscar_failed_password_secure()
    buscar_authentication_failure_messages()
    buscar_errores_carga_paginas_httpd()
    buscar_envio_mails_masivos_maillog()

if __name__ == "__main__":
    main()

import subprocess
def buscar_error_autentificacion():
    output=subprocess.run(["grep","Failed Password","/var/log/secure"],capture_output=True, text=True)
    print(output)

buscar_error_autentificacion()
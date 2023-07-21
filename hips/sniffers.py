import os

def detectar_sniffers():
    sniffers_conocidos = ["tcpdump", "tshark", "wireshark"]

    for sniffer in sniffers_conocidos:
        comando = f"pgrep {sniffer}"
        resultado = os.system(comando)
        
        if resultado != 0:
            print(f"Se ha detectado el proceso '{sniffer}' en ejecución. Esto podría indicar el uso de un sniffer.")
        else:
            print(f"No se ha detectado el proceso '{sniffer}' en ejecución.")
def modo_promiscuo(): 
    resultado = os.popen("cat /var/log/messages | grep -i promis").read().split("\n")
    if resultado[0]=='':
        print(resultado)
    else:
        print("Todo bien")

def main():
    print("Detectando sniffers y modo promiscuo...")
    detectar_sniffers()
    print("Verificando si el sistema entro en modo promiscuo")
    modo_promiscuo()

if __name__ == "__main__":
    main()

import re

def intento_acceso(log_file):
    cant_intentos = {}

    with open(log_file, 'r') as file:
        for line in file:
            if 'password check failed' in line:
                # Usamos split para separar los campos relevantes de la línea
                campos = line.split()
                if len(campos) >= 10:
                    user = campos[5]
                    source_ip = campos[7]
                    key = (user, source_ip)
                    cant_intentos[key] = cant_intentos.get(key, 0) + 1

    return cant_intentos

def main():
    log_file = '/var/log/secure'  # Ruta al archivo de registro de autenticación en CentOS
    cant_intentos = intento_acceso(log_file)

    if not cant_intentos:
        print("No se encontraron intentos de acceso no válidos.")
    else:
        print("Intentos de acceso no válidos:")
        for (user, source_ip), count in cant_intentos.items():
            if user and source_ip:
                print(f"Desde: {source_ip}, Usuario: {user}, Intentos: {count}")
            elif source_ip:
                print(f"Desde: {source_ip}, Usuario: Desconocido, Intentos: {count}")
            else:
                 print(f"Desde: Desconocido, Usuario: {user}, Intentos: {count}")
               

if __name__ == "__main__":
    main()

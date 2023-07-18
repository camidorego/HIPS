import os
import hashlib
import time
import psycopg2

def calcular_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # 64 KB chunks
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def main():
    # Parámetros de conexión a la base de datos
    db_params = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "1234"
    }

    archivo_path = "/home/camidorego/prueba.txt"

    while True:
        try:
            # Conexión a la base de datos
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            # Obtener la firma almacenada en la base de datos
            cursor.execute("SELECT firma FROM fir_archivos WHERE nombre_archivo = %s;", (archivo_path,))
            db_hash = cursor.fetchone()

            # Calcular la firma actual del archivo
            current_hash = calcular_sha256(archivo_path)

            if db_hash:
                db_hash = db_hash[0]  # Extraer el valor de la tupla

            if current_hash != db_hash:
                print("El archivo {} ha sido modificado.".format(archivo_path))

                # Actualizar la firma en la base de datos
                #cursor.execute("UPDATE fir_archivos SET hash = %s WHERE archivo_nombre = %s;", (current_hash, archivo_path))
                conn.commit()
            else:
                print('Tiene la misma firma')

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            print("Error de base de datos:", e)

        # Esperar 1 minutos antes de verificar nuevamente
        time.sleep(60)

if __name__ == "__main__":
    main()

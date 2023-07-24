import psycopg2 
import subprocess
import os
import sys

# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)

import init_db
import hips.escribir_resultado as escribir_resultado

def comparar_firma():
    path_archivo1="/etc/passwd"
    path_archivo2="/etc/shadow"
    
    while True:
        try:
            # conectamos a la base de datos
            conexion = init_db.conectar_bd()

            # creamos el objeto cursor
            cursor=conexion.cursor()

            # extraemos los hashes guardados en la base de datos 
            cursor.execute("SELECT firma FROM firmas WHERE nombre_archivo = %s;", (path_archivo1,))
            hash_original1=cursor.fetchone()

            cursor.execute("SELECT firma FROM firmas WHERE nombre_archivo = %s;", (path_archivo2,))
            hash_original2=cursor.fetchone()

            # calculamos los hashes actuales
            hash_actual1=subprocess.run(["sudo", "sha256sum", path_archivo1], check=True, capture_output=True).stdout.decode().strip().split()[0]
            hash_actual2=subprocess.run(["sudo", "sha256sum", path_archivo2], check=True, capture_output=True).stdout.decode().strip().split()[0]
            
            # comparamos los hashes para ver si los archivos fueron modificados
            if hash_actual1!=hash_original1[0]:
                print("El archivo {path_archivo1} ha sido modificado.")
                
                # se actualiza la base de datos
                cursor.execute("UPDATE firmas SET firma = %s WHERE nombre_archivo = %s;", (hash_actual1, path_archivo1))

                escribir_resultado.guardar_resultado_csv('verificar_firma','controlar_firma',path_archivo1,'fue modificado')
                escribir_resultado.escribir_log('modificacion de archivo binario', f'El archivo {path_archivo1} ha sido modificado')
            elif hash_actual2!=hash_original2[0]:
                print("El archivo {path_archivo2} ha sido modificado.")
                
                # se actualiza la base de datos
                cursor.execute("UPDATE firmas SET firma = %s WHERE nombre_archivo = %s;", (hash_actual2, path_archivo2))
                escribir_resultado.guardar_resultado_csv('verificar_firma','controlar_firma',path_archivo2,'fue modificado')
                escribir_resultado.escribir_log('modificacion de archivo binario', f'El archivo {path_archivo2} ha sido modificado')

            else:
                print("Todo bien")
                escribir_resultado.guardar_resultado_csv('verificar_firma','controlar_firma','ningun archivo','fue modificado')
            
            # se guardan los cambios de la base de datos y se cierra la conexion
            conexion.commit()
            cursor.close()
            conexion.close()

        except psycopg2.Error as e:
            print("Ocurrio un error al conectarse a la BD: ",e)

        # se controlan los hashes cada 5min
        #time.sleep(120) 
        break   

if __name__=="__main__":
    print(sys.path)
    comparar_firma()
    

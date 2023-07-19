import time
import psycopg2 
import calcular_hash

def comparar_firma():

    path_archivo1="/etc/shadow"
    path_archivo2="/etc/passwd"

    while True:
        try:
            conexion = psycopg2.connect(
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432",
                        database="postgres" 
                    )
            cursor=conexion.cursor()

            cursor.execute("SELECT firma FROM firmas WHERE nombre_archivo = %s;", (path_archivo1,))
            hash_original1=cursor.fetchone()

            cursor.execute("SELECT firma FROM firmas WHERE nombre_archivo = %s;", (path_archivo2,))
            hash_original2=cursor.fetchone()

            hash_actual1=calcular_hash.calcular_hash(path_archivo1)
            hash_actual2=calcular_hash.calcular_hash(path_archivo2)

            print(hash_actual1, hash_original1)

            if hash_actual1!=hash_original1[0]:
                respuesta=input(f"El archivo {path_archivo1} ha sido modificado. Estas al tanto de estas modificaciones?(y/n)")
                if(respuesta=='y' or respuesta=='Y'):
                    cursor.execute("UPDATE firmas SET firma = %s WHERE nombre_archivo = %s;", (hash_actual1, path_archivo1))
            
            elif hash_actual2!=hash_original2[0]:
                respuesta=input(f"El archivo {path_archivo2} ha sido modificado. Estas al tanto de estas modificaciones?(y/n)")
                if(respuesta=='y' or respuesta=='Y'):
                    cursor.execute("UPDATE firmas SET firma = %s WHERE nombre_archivo = %s;", (hash_actual2, path_archivo2))

            else:
                print("Todo bien")
            
            conexion.commit()
            cursor.close()
            conexion.close()

        except psycopg2.Error as e:
            print("Ocurrio un error al conectarse a la BD: ",e)

        time.sleep(120)    

if __name__=="__main__":
    comparar_firma()

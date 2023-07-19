import os
import hashlib
import time
import psycopg2 



def calcular_hash(path_archivo):
    hash=hashlib.sha256() # creamos el objeto sha256
    with open(path_archivo, "rb") as f:
    # se genera el hash de todas las lineas concatenadas del archivo 
        while True:
            info=f.read(65536)
            if not info:
                break
            hash.update(info)
        return hash.hexdigest()
    
def crear_tabla():
    try:
        # Conectarse al servidor PostgreSQL
        conexion = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="1234",
            database="postgres"
        )
        
        # Crear un objeto de cursor para ejecutar comandos SQL
        cursor = conexion.cursor()
        
        # Verificar si la tabla existe antes de intentar crearla
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'firmas');")
        tabla_existe = cursor.fetchone()[0]

        if not tabla_existe:
            # Si la tabla no existe, la creamos
            cursor.execute("CREATE TABLE firmas(nombre_archivo varchar(50), firma varchar(64));")
            print("Tabla 'firmas' creada correctamente.")
        
        # Cerrar la conexión y guardar los cambios
        conexion.commit()
        cursor.close()
        conexion.close()
        
    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")


def insertar_info():
    firma1=calcular_hash("/etc/passwd")
    firma2=calcular_hash("/etc/shadow")
    try:
       # Conectarse al servidor PostgreSQL
        conexion = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="1234",
            database="postgres"
        )
        cursor=conexion.cursor()
        print("se conecto")

        #se insertan las firmas
        cursor.execute("INSERT INTO firmas(nombre_archivo, firma) VALUES (%s, %s), (%s, %s);",
                   ('/etc/passwd', firma1, '/etc/shadow', firma2))
        print('Se inserto')
        conexion.commit()
        cursor.close()
        conexion.close()
    except psycopg2.Error as e:
        print("Ocurrio un error al conectarse al insertar la informacion a la tabla: ",e)

def comparar_actual():

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

            hash_actual1=calcular_hash(path_archivo1)
            hash_actual2=calcular_hash(path_archivo2)

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
    crear_tabla()
    insertar_info()
    comparar_actual()

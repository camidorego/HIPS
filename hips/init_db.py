import psycopg2 
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def conectar_bd():
    try:
    # conectamos a la base de datos
        conexion= psycopg2.connect(
                host="localhost",
                database="hips",
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWD'))
        
    except psycopg2.Error as e:
        print(f"Error al conectar a la bd: {e}")

    return conexion

def crear_tabla_users():
    try:
        conexion=conectar_bd()

        # creamos el objeto cursor para manipular la base de datos
        cursor = conexion.cursor()

        # creamos la tabla users
        cursor.execute('DROP TABLE IF EXISTS users;')
        cursor.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                        'nombre varchar (150) NOT NULL,'
                                        'username varchar (150) NOT NULL,'
                                        'password varchar (50) NOT NULL,'
                                        'email varchar (50) NOT NULL);'
                                        )

        # insertamos los datos del administrador
        cursor.execute("INSERT INTO users (nombre,username,password,email) VALUES ('admi','admi', 'passwd','camidoregob@gmail.com');")

        # guardamos los cambios
        conexion.commit()

        # cerramos la conexion
        cursor.close()
        conexion.close()

    except psycopg2.Error as e:
        print(f"Error al crear la tabla users: {e}")


def crear_tabla_firmas():
    firma1=subprocess.run(["sudo", "sha256sum", "/etc/passwd"], check=True, capture_output=True).stdout.decode().strip().split()[0]
    firma2=subprocess.run(["sudo", "sha256sum", "/etc/shadow"], check=True, capture_output=True).stdout.decode().strip().split()[0]
    try:
        # conectamos a la bd
        conexion = conectar_bd()
        
        # creamos el objeto cursor para manipular la bd
        cursor = conexion.cursor()

        # creamos la tabla firmas
        cursor.execute('DROP TABLE IF EXISTS firmas;')
        cursor.execute("CREATE TABLE firmas(nombre_archivo varchar(50), firma varchar(64));")
        print("Tabla 'firmas' creada correctamente.")

        #se insertan las firmas
        cursor.execute("INSERT INTO firmas(nombre_archivo, firma) VALUES (%s, %s), (%s, %s);",
                ('/etc/passwd', firma1, '/etc/shadow', firma2))
        print('Se inserto')
        
        # guardamos los cambios y cerramos la conexion
        conexion.commit()
        cursor.close()
        conexion.close()
        
    except psycopg2.Error as e:
        print(f"Error al crear la tabla firmas: {e}")

if __name__=="__main__":
    crear_tabla_users()
    crear_tabla_firmas()
   


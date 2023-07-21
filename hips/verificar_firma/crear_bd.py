import psycopg2 
import calcular_hash

def crear_tabla():
    firma1=calcular_hash.calcular_hash("/etc/passwd")
    firma2=calcular_hash.calcular_hash("/etc/shadow")
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
            tabla_existe=True
        
            #se insertan las firmas
            cursor.execute("INSERT INTO firmas(nombre_archivo, firma) VALUES (%s, %s), (%s, %s);",
                ('/etc/passwd', firma1, '/etc/shadow', firma2))
            print('Se inserto')
        
        # Cerrar la conexión y guardar los cambios
        conexion.commit()
        cursor.close()
        conexion.close()
        
    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")
    return tabla_existe
if __name__=="__main__":
    crear_tabla()


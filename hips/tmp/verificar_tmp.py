import os
import shutil
import sys
# directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# directorio hips
parent_dir = os.path.dirname(current_dir)

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(parent_dir)
import escribir_resultado

# directorio controlar_logs
logs_dir = os.path.join(parent_dir, 'controlar_logs')
sys.path.append(logs_dir)
import acciones

def ver_extension(archivo):
    # verificamos la extension del archivo
    script_extensions = ['.sh', '.py', '.pl', '.rb', '.bat', '.cmd']
    return any(archivo.endswith(ext) for ext in script_extensions)

def verificar_tmp():
    path = '/tmp'
    dir_cuarentena = '/tmp/quarantine'
    
    # creamos el directorio cuarentena si no existe
    if not os.path.exists(dir_cuarentena):
        os.makedirs(dir_cuarentena)
    
    suspicious_files = []
    
    # revisamos los archivos en /tmp
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath) and ver_extension(filename):
            suspicious_files.append(filename)
    
    # se analiza el resultado
    if not suspicious_files:
        print("No se encontraron archivos sospechosos en /tmp.")
        escribir_resultado.guardar_resultado_csv('tmp','verificar_tmp',"No se encontraron archivos sospechosos en /tmp.",'')
    else:
        print("Archivos sospechosos encontrados:")
        # si se encontraron archivos sospechosos se imprime y se mueven los archivos al directorio de cuarentena
        for filename in suspicious_files:
            print(f" - {filename}")
            # se guarda el resultado en los logs
            escribir_resultado.guardar_resultado_csv('tmp','verificar_tmp','Se encontro el siguiente archivo sospechoso',filename)
            escribir_resultado.escribir_log('Posible Malware', f'Se encontro el siguiente archivo sospechoso en /tmp {filename}')
            
            # se mueve a la carpeta de cuarentena
            src_filepath = os.path.join(path, filename)
            dest_filepath = os.path.join(dir_cuarentena, filename)
            shutil.move(src_filepath, dest_filepath)
            escribir_resultado.escribir_prevencion(f'Se movio el archivo {filename} a una carpeta de cuarentena')

            
            

        print("Archivos movidos a la cuarentena.")
        print("Se le informara al administrador de esta situacion")

        # se le informa al administrador
        acciones.enviar_mail('Alarma!','Posible Malware',f'Se encontraron los siguientes archivo sospechoso en /tmp {suspicious_files}. Por seguridad fue movido a una carpeta de cuarentena')
        

if __name__ == "__main__":
    verificar_tmp()

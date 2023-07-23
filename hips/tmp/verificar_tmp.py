import os
import shutil
import escribir_csv

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
    
    if not suspicious_files:
        print("No se encontraron archivos sospechosos en /tmp.")
    else:
        print("Archivos sospechosos encontrados:")
        # si se encontraron archivos sospechosos se imprime y se mueven los archivos al directorio de cuarentena
        for filename in suspicious_files:
            print(f" - {filename}")
            escribir_csv.guardar_resultado_csv('verificar_procesos','scripts_sospechosos',filename,'')
        
        for filename in suspicious_files:
            src_filepath = os.path.join(path, filename)
            dest_filepath = os.path.join(dir_cuarentena, filename)
            shutil.move(src_filepath, dest_filepath)
        print("Archivos movidos a la cuarentena.")
        print("Se le informara al administrador de esta situacion")

        #enviar correo
        

if __name__ == "__main__":
    verificar_tmp()

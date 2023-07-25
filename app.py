from flask import Flask, render_template, request, redirect, url_for, session
import csv
import psycopg2
import subprocess
import os
import sys
from pathlib import Path

# directorio actual /HIPS/
current_dir = os.path.dirname(os.path.abspath(__file__))

# Convierte current_dir en un objeto Path
current_dir = Path(current_dir)

# path de /HIPS/hips/
hips_dir = os.path.join(current_dir, 'hips')
# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(str(hips_dir))

import init_db

from dotenv import load_dotenv

load_dotenv()

# creamos nuestro objeto Flask
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

# definimos nuestra url /login que puede tener metodos de GET y POST 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # guardamos el username y la contrasena que introdujo en usuarios
        username = request.form['username']
        password = request.form['password']

        # nos conectamos a la base de datos
        conn = init_db.conectar_bd()
        cur = conn.cursor()

        # hacemos un query para ver si la informacion esta en la base de datos
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

        # si devuelve algo el query se guarda en user
        user = cur.fetchall()

        # cerramos la conexion
        cur.close()
        conn.close()

        # si user no es vacio es porque la informacion de login es correcta y se le redirige al usuario al menu
        if user:
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    
    # si el metodo es de GET se muestra la interfaz de login
    else:
        return render_template('login.html')

# definimos nuestra url register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # se guardan los datos introducidos por el usuario
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # se conecta a la base de datos
        conn = init_db.conectar_bd()
        cur = conn.cursor()

        # hacemos un query para guardar la informacion del usuario
        cur.execute("INSERT INTO users (nombre,username,password,email) VALUES (%s,%s,%s,%s);",(name,username,password,email,))

        # guardamos los cambios de la base de datos
        conn.commit()

        # cerramos la conexion
        cur.close()
        conn.close()

        return render_template('login.html')

    else:
        return render_template('register.html')


# definimos nuestro url del menu
@app.route('/index')
def index():
    # se muestra la interfaz del menu
    return render_template('index.html')

# funcion para leer los resultados de los archivos .csv
def cargar_datos_desde_csv(nombre_archivo):
    # cargamos los datos del archivo y se retorna una lista de filas
    datos = []
    with open(nombre_archivo, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for fila in reader:
            datos.append(fila)
    return datos

# definimos la url de cada vez que se aprieta un boton de Verificar
@app.route('/<folder>/<program_name>')
def ejecutar_herramienta(folder,program_name):
    # se ejecuta la herramienta correspondiente
    subprocess.run(["python3", f"./hips/{folder}/{program_name}.py"])
    # llamamos a la funcion para leer el csv
    datos = cargar_datos_desde_csv(f"/var/log/hips/resultados/{folder}/{program_name}.csv")
    # se muestran los datos en la interfaz de resultado
    return render_template('resultado.html', datos=datos)

# definimos la url root
@app.route('/')
def root():
    # se redirecciona a la pagina de login
    return redirect(url_for('login'))

# nuestra funcion main
if __name__ == '__main__':
    # se inicializa la base de datos con la informacion del administrador
    init_db.crear_tabla_users()
    # y las firmas de los archivos binarios
    init_db.crear_tabla_firmas()
    # se ejecuta la aplicacion
    app.run(debug=True)

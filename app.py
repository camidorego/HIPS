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
dir_hips = current_dir.joinpath('hips')

# agregamos el path /hips a los directorios donde se buscaran los modulos
sys.path.append(str(dir_hips))

import init_db


app = Flask(__name__)
app.secret_key = 'secret'

def get_db_connection():
    # Create a new database connection for each request
    print("hola DB")
    con=psycopg2.connect(
        host="localhost",
        database="hips",
        user="hips",
        password="12345"
    )
    return con


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get the database connection from the session
        conn = get_db_connection()
        cur = conn.cursor()

        # Query the database for the user
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchall()

        # Close the cursor (optional, but recommended)
        cur.close()
        conn.close()

        if user:
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Get the database connection from the session
        conn = get_db_connection()
        cur = conn.cursor()

        # Query the database for the user
        cur.execute("INSERT INTO users (nombre,username,password,email) VALUES (%s,%s,%s,%s);",(name,username,password,email,))

        conn.commit()

        # Close the cursor (optional, but recommended)
        cur.close()
        conn.close()

        return render_template('login.html')

    else:
        return render_template('register.html')



@app.route('/index')
def index():
    
    return render_template('index.html')

def cargar_datos_desde_csv(nombre_archivo):
    # Carga los datos del archivo CSV y retorna una lista de filas
    datos = []
    with open(nombre_archivo, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for fila in reader:
            datos.append(fila)
    return datos

@app.route('/<folder>/<program_name>')
def ejecutar_herramienta(folder,program_name):
    subprocess.run(["python3", f"./hips/{folder}/{program_name}.py"])
    datos = cargar_datos_desde_csv(f"/var/log/hips/resultados/{folder}/{program_name}.csv")
    return render_template('resultado.html', datos=datos)


@app.route('/')
def root():
    # Check if the user is logged in
    if 'user_id' in session:
        # If the user is logged in, redirect to the dashboard page
        return redirect(url_for('index'))
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))


if __name__ == '__main__':
    init_db.crear_tabla_users()
    init_db.crear_tabla_firmas()
    app.run(debug=True)

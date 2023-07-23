import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="hips",
        user="hips",
        password="12345")
        #user=os.environ['DB_USERNAME'],
        #password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'nombre varchar (150) NOT NULL,'
                                 'username varchar (150) NOT NULL,'
                                 'password varchar (50) NOT NULL,'
                                 'email varchar (50) NOT NULL);'
                                 )

# Insert data into the table

cur.execute("INSERT INTO users (nombre,username,password,email) VALUES ('admi','admi', 'passwd','camidoregob@gmail.com');")

conn.commit()

cur.close()
conn.close()

# Sistema de Deteccion y Prevencion de Intrusos
## Acerca de este Proyecto
Este es un proyecto desarrollado para la materia Sistemas Operativos 2 de la Universidad Católica de Asunción con el propósito de aprender a defender un sistemas de posibles intrusos y todo lo que ello implica.

Los puntos cubridos en el sistema son:

 - Verificar archivos binarios de sistema y en particular modificaciones realizadas
en el archivo /etc/passwd o /etc/shadow.
 - Verificar los usuarios conectados al sistema y sus respectivos origenes.
 - Verificar si hay sniffers en el sistema:
	 - Se verifica se estan ejecutando herramientas de acaptura de paquetes conocidas como 'tcpdump', 'ethereal', 'wireshark'
	 - Se verifica si el sistema entro en modo promiscuo
 - Se examinan los logs del sistema en busca de patrones de accesos indebidos. Los logs examinados son:
	 - /var/log/secure
	 - /var/log/messages
	 - /var/log/httpd/access_log
	 - /var/log/maillog
 - Se verifica el tamaño de la cola de mail en busca de envios de correos masivos desde una misma direccion
 - Se revisa el consumo de los recursos del sistema, controlando los procesos que consumen demasiada memoria
 - En el directorio /tmp buscamos archivos sospechosos que podrian estar ejecutandose
 - Controlamos la presencia de Ataquea Distribuidoa de Denegación de Servicio
 - Examinamos que los archivos en ejecutacion como cron
 - Se verifican intentos de accesos indebidos
 

### Este sistema fue construido con:

 - Python
 - Bootstrap
 - Flask
 - PostgreSQL


##  Pre-requisitos

#### Del sistema:

 - Centos 9
 - Tener acceso como usuario root

#### Python3

Instalar instalar Python3 y Pip3

    sudo yum install python3
    sudo yum install python3-pip
##### Intalación de modulos de Python

Psycopg2: necesario para trabajar con la base de datos
 

    pip3 install --user psycopg2

 Flask
 

    pip3 install --user flask
dotenv

    pip3 install --user python-dotenv

#### PostgreSQL
Instalar y configurar PostgreSQL


    sudo yum install postgresql
    sudo yum install postgresql-server
  
Creamos un nuevo cluster de la base de datos PostgreSQL

    sudo systemctl start postgresql

Iniciamos y habilitamos el servicio de postgres

    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    
##### Ahora debemos configurar la Base de Datos
Iniciamos con la cuenta de postgres

    sudo -i -u postgres

Creamos un nuevo rol

    create user hips with password '<BD_HIPS_PASSWD>';
Creamos una base de datos

    createdb hips
Le asgnamos los permisos necesarios al rol hips

    GRANT ALL PRIVILEGES ON DATABASE hips TO hips;

#### IPTables
Se para el servicio de firewalld

    sudo systemctl stop firewalld
Se desabilita

    sudo systemctl disable firewalld
Maskeamos para evitar que otro programa lo invoque

    sudo systemctl mask --now firewalld
Intalamos IPTables

    sudo yum install iptables-services -y
Iniciamos y habilitamos el servicio

    sudo systemctl start iptables
    sudo systemctl enable iptables
    sudo systemctl start ip6tables
    sudo systemctl enable ip6tables
Verificamos que este funcionando

    sudo systemctl status iptables
    sudo systemctl status ip6tables

#### Crontab

    sudo yum install cronie

## Instalacion

Descarga el programa en tu Desktop.

    git clone https://github.com/camidorego/HIPS.git
Entra dentro del directorio y establece la contrasena que elegiste para la base de datos

    cd HIPS
    nano .env
    DB_PASSWDD='<contraseña>'
    
Guarda el archivo y cambia los permisos para que solo root pueda revisar el archivo

   

    sudo su
    chmod 700 .env


## Directorios Necesarios

Necesitamos crear algunos directorios donde el sistema guardara los resultados, las alarmas y los metodos de prevencion.

Estando como usuario root

    mkdir /var/log/hips
    mkdir /var/log/hips/resultados
    mkdir /var/log/hips/resultados/accesos
    mkdir /var/log/hips/resultados/controlar?logs
    mkdir /var/log/hips/resultados/cron
    mkdir /var/log/hips/resultados/ddoc
    mkdir /var/log/hips/resultados/procesos
    mkdir /var/log/hips/resultados/sniffer
    mkdir /var/log/hips/resultados/tmp
    mkdir /var/log/hips/resultados/usuarios_conectados
    mkdir /var/log/hips/resultados/ver_cola_mail
    mkdir /var/log/hips/resultados/verificar_firma

Crear los logs

    touch mkdir /var/log/hips/alarmas.log

    touch /var/log/hips/prevencion.log
    
## Modo de Uso
Estando como root en la carpeta HIPS

     export FLASK_APP=app
     flask run

En el navegador abre el siguiente link
   

    http://127.0.0.1:5000

Te aparecera la pagina para logearte
<p align="center">
  <a href="">
    <img src="./static/images/login.png" alt="Login" width="1600" height="500">
  </a>
</p>


Puedes crear una cuenta. Aprieta el boton de Crear Cuenta y te llevara a la pagina para registrarte
<p align="center">
  <a href="">
    <img src="./static/images/register.png" alt="Register" width="1600" height="500">
  </a>
</p>

Una vez que completaste tu informacion se te llevara nuevamente a la pagina para que puedas logearte con el username y contraseña que recien creaste

Luego te aparecera el menu. Elige lo que quieres controlar y listo!
<p align="center">
  <a href="">
    <img src="./static/images/menu.png" alt="Menu" width="1600" height="500">
</p>


## Informacion del Programador
           

Camila Do Rego Barros

Correo: camiladoregobarros@gmail.com

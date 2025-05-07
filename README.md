# PROYECTO
Entrega de proyecto de API con consultas MYSQL con Databases
#GUIA PARA LEVANTAR LOS ARCHIVOS
Primero descarga todos los archivos que estan en este repositorio, los cuales contaran con la siguiente estructura:

├── database.py              # Conexión y funciones para interactuar con la base de datos

├── docker-compose.yml       # Configuración de servicios Docker

├── formato.py               # Funciones para formatear tablas HTML

├── main.py                  # Aplicación FastAPI principal con endpoints

├── pandas_consultas.py      # Consultas usando pandas

├── requirements.txt         # Dependencias de Python

├── seaborn_consultas.py     # Consultas con visualizaciones usando seaborn

├── verify_db_connection.py  # Script para verificar la conexión a la base de datos

└── sql/                     # Directorio con scripts SQL (mencionado en docker-compose.yml)
    └── #Aca estaran los archivos sql de las tablas de la carpeta
    
Una vez unstalados usa en la terminal con ubicacion a la carpeta de todos estos archivos el comando: "Docker-compose up -d".

De esa manera deberia poder subirse todo el contenido sin problemas, verifica que sea desde un sistema completo de Linux Ubuntu, ya que hemos verificado que utilizar maquinas virtuales o emuladores de Linux provocan fallos inesperados y puede no funcionar correctamente.

EL SERVICIO FAST API ESTA EN el puerto: 8087
EL SERVIDOR phpmyadmin esta en el puerto: 8088
LA BASE DE DATOS esta en el puerto: 3309

#Descripcion de Archivos
-main.py: Es el principal punto de entrada del FastAPI, al igual que define las tablas.

-dockerfile: Esta ligada con la instalacion de las dependencias utilizadas para FastAPI como pandas

-requirements.txt: Son las Dependencias para FastAPI que usara el Dockerfile

-docker-compose.yml: Este archivo es la conexion y relacion que hay entre los servicios(MYSQL, PHPmyAdmind y FastAPI)

-database.py: Este modulo ayuda a la conexion entre la base de datos y el servicio principal MYSQL

-pandas_consultas.py: Aqui se realizan consultas de tablas avanzadas con la libreria Pandas

-seaborn_consultas.py: Aca se realizan las graficas de varias consultas en el servici, generando graficos de distinto tipo

-verify_db_connection: Este archivo ayuda a evitar posibles malos alzamientos del servicio MYSQL con FastAPI

-formato.py: Este archivo convierte las tablas y sus funciones en tablas HTML

NOTA: ES IMPORTANTE TENER INSTALADO DOCKER

##USO DE LOS SERVICIOS DE FASTAPI
Al acceder al FastAPI puedes realizar varias consultas como: Lista de superheroes con mas poderes, empresas con mas superpoderes y muchomas
Solo debes acceder a alguna de tu interes y seleccionar Try y seleccionar la cantidad maxima de columnas, ahi se generara un link HTML el cual puedes copiar para acceder a la tabla.
Esto tambien funciona con las graficas en seaborn.


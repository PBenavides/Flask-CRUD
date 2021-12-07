# Flask-CRUD
Flask Crud with MongoDB and Oracle Database

Para ejecutar la aplicación se necesita tener instalado Oracle Express y MongoDB los cuales en cada caso tienen que estar desplegados y con endpoints en:

ORACLE XE: En el puerto 1521 con el usuario system y la contraseña admin. localhost:1521/xe

MongoDB: En el puerto 27017, en este caso el nombre de la base de datos será pythonmongodb.

Una vez instaladas estas dos bases de datos, se deberá ejecutar dentro de Oracle el archivo dentro de sql/script.sql

Se recomienda el uso de entorno virtual
```bash
$ python3 -m venv venv
$ ./venv/scripts/activate
```

Posteriormente se deberá instalar todas las librerías y dependencias desde el manejador de paquetes pip. Recordar que para esto, se estará dentro de la carpeta del proyecto.
```bash
$ pip install > requirements.txt
```

Por último la aplicación se inicializa con flask de la siguiente forma.
```bash
$ flask run
```

Luego, se podrá ver e interactuar con la aplicación en: http://127.0.0.1:5000/


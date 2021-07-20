# vacunas-argentina-covid

Comandos para instalar dependencias:

En caso de no tener python instalado, instalar python, o buscar algun entorno de python mas conveniente:

```sh
sudo apt-get install libpq-dev python-dev
```

Luego instalar las dependencias del proyecto

```sh
sudo pip install -r requirements.txt
```

Comando para levantar la API desde server/:
```sh
cd server
uvicorn main:app --reload
```

Comando para actualizar la DB.

Para configurar la conexion a la db, se debe crear el archivo .env con el host, usuario y clave. Se recomienda renombrar el archivo .env.example a .env, y cambiar los valores segun sea adecuado.

Si se lo deja corriendo, cada 24 hrs volverá a bajar los datos:
```sh
python3 server/api/update_db.py
```

##[Swagger](https://shipupi.github.io/vacunas-argentina-covid/swagger/)
# vacunas-argentina-covid

Comandos para instalar dependencias:
```sh
sudo apt-get install libpq-dev python-dev
pip3 install fastapi
pip3 install uvicorn
pip3 install schedule
pip3 install psycopg2
```

Comando para levantar la API desde src/api:
```sh
uvicorn main:app --reload
```

Comando para actualizar la DB.
Los datos de la DB se configuran desde src/config/database.ini
Si se lo deja corriendo, cada 24 hrs volverá a bajar los datos:
```sh
python3 src/api/update_db.py
```

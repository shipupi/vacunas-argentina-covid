# vacunas-argentina-covid

# TO DO:
* Crear Endpoints
* Hacer visualizaciones (probar que la tabla geodata tenga bien los datos)
* Resolver bug donde al descargar nomivac a veces dice "File is not a zip file"

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


## Endpoints / Graficos a mostrar


*Choropleth por departamento/provincia*
/dosisPorProvincia
```json
[
    {
        "nombre": "Buenos Aires",
        "dosis": 10000,
        "geospacial": {
            //....
        }
    }
]
```

/provinces

```json
[
    {
        "id": 1,
        "pronvice": "buenos aires"
    }
]
```

/dosisPorDepartamento/:provinceId

```json
[
    {
        "nombre": "La matanza",
        "dosis": 5000,
        "geospacial": {
            //....
        }
    },
    //etc
]
```

/brands devuelve un vector de brands

```json
[
    {
        "id": 1,
        "brand": "sputnik"
    },
]
```

/demoradeaplicacion/:brandId?
brandId es opcional, sin brandId devuelve vector de todas
```json
[
    {
        "marca": "sputnik",
        "evolucion": [
            {
                "fecha": "01-02-2020",
                "recibidas": 20000,
                "aplicadas": 50
            }
        ]
    }
]
```

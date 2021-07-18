# vacunas-argentina-covid

# TO DO:
* Hacer visualizaciones (probar que la tabla geodata tenga bien los datos)
* Resolver bug donde al descargar nomivac a veces dice "File is not a zip file"

Comandos para instalar dependencias:

En caso de no tener python instalado, instalar python, o buscar algun entorno de python mas conveniente:

```sh
sudo apt-get install libpq-dev python-dev
```

Luego instalar las dependencias del proyecto

```sh
pip install -r requirements.txt
```

Comando para levantar la API desde server/:
```sh
uvicorn main:app --reload
```

Comando para actualizar la DB.

Para configurar la conexion a la db, se debe crear el archivo .env con el host, usuario y clave. Se recomienda renombrar el archivo .env.example a .env, y cambiar los valores segun sea adecuado.

Si se lo deja corriendo, cada 24 hrs volverá a bajar los datos:
```sh
python3 server/api/update_db.py
```

## Endpoints / Graficos a mostrar


*Choropleth por departamento/provincia*
/provinces/vaccines

Queryparams:
- ProvinceId (optional - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
Response: 
```json
[
    {
        "nombre": "Buenos Aires",
        "primera_dosis": 10000,
        "segunda_dosis": 10000,
        "total_dosis": 20000,
    }
    // ... Demas provincias
]
```

*Choropleth de provincias*: Se adjuntan los datos geoespaciales de las provincias, para poder dibujar el pais junto con los datos de cada provincia
/provinces/vaccines_geo

Response: 
```json
[
    {
        "nombre": "Buenos Aires",
        "primera_dosis": 10000,
        "segunda_dosis": 10000,
        "total_dosis": 10000,
        "geo": //geodata...
    }
    // ... Demas provincias
]
```

/provinces
```json
[
    {
        "id": "06",
        "pronvice": "buenos aires"
    }
]
```

/departments
Lista los departamentos
- ProvinceId (Optional - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
```json
[
  {
    "gid": 245,
    "fna": "Comuna 14",
    "gna": "Comuna",
    "nam": "Comuna 14",
    "inl": "02098",
    "fdc": "Direc. de Catastro",
    "sag": "IGN"
  },
  // ...
```


*Choropleth de departamentos*: Se adjuntan los datos geoespaciales a los departamentos de una provincia,  para poder dibujar la provincia, junto con sus datos por cada departamento
/departments/vaccines_geo

Queryparams:
- ProvinceId (required - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
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

/brand_timelilne
Timeline devuelve dia a dia las aplicaciones de cada vacuna, separado por primera dosis o segunda dosis y por la marca de la vacuna
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

/arrivals
Timeline de arrival de vacunas, separado por marca de vacuna
```json
[
  {
    "empresa": "LIMITED LIABILITY COMPANY HUMAN VACCINE",
    "cantidad": 765545,
    "guia_aerea": "044-44033150",
    "fecha_entrega": "2021-04-29",
    "empresa_traslado": "None",
    "vaccine_id": 1,
    "nomivac_name": "Sputnik",
    "actas_de_recepcion_name": "LIMITED LIABILITY COMPANY HUMAN VACCINE"
  },
  {
    "empresa": "LIMITED LIABILITY COMPANY HUMAN VACCINE",
    "cantidad": 800000,
    "guia_aerea": "044-44033124",
    "fecha_entrega": "2021-04-18",
    "empresa_traslado": "Aerolíneas Argentinas",
    "vaccine_id": 1,
    "nomivac_name": "Sputnik",
    "actas_de_recepcion_name": "LIMITED LIABILITY COMPANY HUMAN VACCINE"
  }
  ```

/timeline
Devuelve una timeline con todas las marcas agregadas. Y el acumulado de vacunas y porcentaje vacunados
```json

```
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
- province (optional - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
Response:
```json
[
    {
        "jurisdiccion_codigo_indec": "30",
        "jurisdiccion_nombre": "Entre Ríos",
        "primera_dosis": 615881,
        "segunda_dosis": 161235,
        "total_dosis": 777116,
        "poblacion": 1345293,
        "porc_primera_dosis": 45.78,
        "porc_ambas_dosis": 11.99
    },
    // ... Demas provincias
]
```

*Choropleth de provincias*: Se adjuntan los datos geoespaciales de las provincias, para poder dibujar el pais junto con los datos de cada provincia
/provinces/vaccines_geo

Response:
```json
[
    {
        "jurisdiccion_codigo_indec":"38",
        "jurisdiccion_nombre":"Jujuy",
        "primera_dosis":371220,
        "segunda_dosis":101836,
        "poblacion":779212,
        "geometry": //geodata...
    },
    // ... Demas provincias
]
```

/provinces
```json
[
    {
        nam: "Ciudad Autónoma de Buenos Aires",
        inl: "02"
    },
    {
        nam: "Neuquén",
        inl: "58"
    },
    // ... Demas provincias
]
```

/departments
Lista los departamentos
- province (Optional - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
```json
[
    {
        "provincia": "Buenos Aires",
        "provinciaid": "06",
        "nam": "General Lavalle",
        "inl": "06336",
        "poblacion": 4528
    },
  // ...
]
```

/departments
Lista los departamentos y sus datos de vacunación
- province (Optional - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
```json
[
    {
        "jurisdiccion_residencia": "Buenos Aires",
        "jurisdiccion_residencia_id": "06",
        "depto_residencia": "Adolfo Alsina",
        "depto_residencia_id": "007",
        "codigo_indec": "06007",
        "provincia": "Buenos Aires",
        "provinciaid": "06",
        "poblacion": 17507,
        "primera_dosis": 10588,
        "segunda_dosis": 3249,
        "porc_primera_dosis": 60.48,
        "porc_ambas_dosis": 18.56
    },
    // ...
]
```

*Choropleth de departamentos*: Se adjuntan los datos geoespaciales a los departamentos de una provincia,  para poder dibujar la provincia, junto con sus datos por cada departamento
/departments/vaccines_geo

Queryparams:
- province (required - string): Se filtra por una provincia en particular. Utilizando los Ids de provincia de Indec. Se pueden consultar en el endpoint /provinces
```json
[
    {
        "jurisdiccion_residencia": "CABA",
        "jurisdiccion_residencia_id": "02",
        "depto_residencia": "COMUNA 12",
        "codigo_indec": "02084",
        "depto_residencia_id": "084",
        "cantidad": 12475,
        "poblacion": 215002,
        "orden_dosis": 2,
        "geometry": {
            //...
        }
    },
    //...
]
```

/brand_timeline
Timeline devuelve dia a dia las aplicaciones de cada vacuna, separado por primera dosis o segunda dosis y por la marca de la vacuna
```json
[
    {
        "fecha_aplicacion": "2020-12-29",
        "orden_dosis": 1,
        "vacuna": "COVISHIELD",
        "cantidad": 1
    },
    {
        "fecha_aplicacion": "2020-12-29",
        "orden_dosis": 1,
        "vacuna": "Sputnik",
        "cantidad": 20446
    },
    {
        "fecha_aplicacion": "2020-12-29",
        "orden_dosis": 2,
        "vacuna": "Sputnik",
        "cantidad": 2
    },
    //...
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
  },
  // ...
]
```

/timeline
Devuelve una timeline con todas las marcas agregadas. Y el acumulado de vacunas y porcentaje vacunados
```json
[
    {
        "fecha": "2020-12-29",
        "primera_dosis": 20447,
        "acum_primera_dosis": 20447,
        "segunda_dosis": 2,
        "acum_segunda_dosis": 2
    },
    {
        "fecha": "2020-12-30",
        "primera_dosis": 20044,
        "acum_primera_dosis": 40491,
        "segunda_dosis": 0,
        "acum_segunda_dosis": 2
    },
    {
        "fecha": "2020-12-31",
        "primera_dosis": 2805,
        "acum_primera_dosis": 43296,
        "segunda_dosis": 0,
        "acum_segunda_dosis": 2
    },
    {
        "fecha": "2021-01-01",
        "primera_dosis": 121,
        "acum_primera_dosis": 43417,
        "segunda_dosis": 0,
        "acum_segunda_dosis": 2
    },
    {
        "fecha": "2021-01-02",
        "primera_dosis": 3286,
        "acum_primera_dosis": 46703,
        "segunda_dosis": 1,
        "acum_segunda_dosis": 3
    },
    // ...
]
```

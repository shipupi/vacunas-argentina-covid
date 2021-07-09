import psycopg2
from fastapi import FastAPI
from enum import Enum
from update_db import config

def build_dict(cursor, row):
    x = {}
    for key,col in enumerate(cursor.description):
        x[col[0]] = row[key]
    return d

def run_query(query):
    conn = None
    results = []
    try:
        params = config(filename="../config/database.ini")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        columns = list(cur.description)
        result = cur.fetchall()
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            results.append(row_dict)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return results

app = FastAPI()

# GET ALL VACCINE ARRIVAL DATA
@app.get("/arrivals")
async def get_arrivals():
    return run_query("SELECT * FROM actas_de_recepcion_vacunas")

# TEMPLATES
@app.get("/")
async def root():
    return {"message": "Hello World"}

# For path params
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# For query params
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# For enums
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

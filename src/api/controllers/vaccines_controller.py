from fastapi import APIRouter
from typing import Optional
from api.services.vaccines_service import get_arrivals

router = APIRouter()

# GET ALL VACCINE ARRIVAL DATA
@router.get("/arrivals")
async def list_arrivals():
    arrivals = get_arrivals()
    return arrivals




# from enum import Enum
# def build_dict(cursor, row):
#     x = {}
#     for key,col in enumerate(cursor.description):
#         x[col[0]] = row[key]
#     return d



# # TEMPLATES
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # For path params
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# # For query params
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# # For enums
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#     return {"model_name": model_name, "message": "Have some residuals"}

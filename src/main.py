from api.controllers import vaccines_controller
from fastapi import FastAPI


app = FastAPI()
app.include_router(vaccines_controller.router)


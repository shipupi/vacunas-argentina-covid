from api.controllers import vaccines_controller
from api.controllers import province_controller
from api.controllers import department_controller
from fastapi import FastAPI


app = FastAPI()
app.include_router(vaccines_controller.router)
app.include_router(province_controller.router)
app.include_router(department_controller.router)


from api.controllers import vaccines_controller
from api.controllers import province_controller
from api.controllers import department_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(vaccines_controller.router)
app.include_router(province_controller.router)
app.include_router(department_controller.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import APIRouter
from typing import Optional
from api.services.department_service import get_province_geospatial


router = APIRouter()

@router.get("/department/vaccines_geo")
async def list_vaccines_geo(province: str):
    # Get data
    vaccines = get_province_geospatial(province)
    return vaccines
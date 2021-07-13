from fastapi import APIRouter
from typing import Optional
from api.services.provinces_service import get_provinces, get_vaccines_by_province
from api.controllers.helpers import validate_bool_param

router = APIRouter()

@router.get("/provinces")
async def list_provinces():
    provinces = get_provinces()
    return provinces

@router.get("/provinces/vaccines")
async def list_vaccines(province: Optional[str] = None, geospatial: Optional[str] = None, department: Optional[str] = None):
    # Validate query params
    # province = validate_int_parameter(province)
    geospatial = validate_bool_param(geospatial)

    # Get data
    vaccines = get_vaccines_by_province(province=province, geospatial=geospatial)
    return vaccines
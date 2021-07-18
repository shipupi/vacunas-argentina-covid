from fastapi import APIRouter
from typing import Optional
from api.services.provinces_service import get_provinces, get_vaccines_by_province, get_all_vaccines_geodata, get_vaccines_by_single_province
from api.controllers.helpers import validate_bool_param

router = APIRouter()

@router.get("/provinces")
async def list_provinces():
    provinces = get_provinces()
    return provinces

@router.get("/provinces/vaccines")
async def list_vaccines(province: Optional[str] = None):
    # Get data
    if province:
        vaccines = get_vaccines_by_single_province(province)
    else:
        vaccines = get_vaccines_by_province(province=province)

    return vaccines

@router.get("/provinces/vaccines_geo")
async def list_vaccines_geo(province: Optional[str] = None):
    # Get data
    vaccines = get_all_vaccines_geodata()
    return vaccines

@router.get("/provinces/vaccines")
async def list_vaccines(province: Optional[str] = None, geodata: Optional[str] = None, department: Optional[str] = None):
    # Validate query params
    # province = validate_int_parameter(province)
    geodata = validate_bool_param(geodata)

    # Get data
    vaccines = get_vaccines_by_province(province=province, geospatial=geodata)
    return vaccines
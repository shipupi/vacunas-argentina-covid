from fastapi import APIRouter
from typing import Optional
from api.services.department_service import get_departments_by_province, get_province_geospatial, get_departments, get_vaccines_by_department


router = APIRouter()

@router.get("/departments")
async def list_departments(province: Optional[str] = None):
    if province:
        departments = get_departments_by_province(province)
    else:
        departments = get_departments()
    return departments

@router.get("/departments/vaccines_geo")
async def list_vaccines_geo(province: str):
    # Get data
    vaccines = get_province_geospatial(province)
    return vaccines

@router.get("/departments/vaccines")
async def list_vaccines(province: str):
    # Get data
    vaccines = get_vaccines_by_department(province)
    return vaccines
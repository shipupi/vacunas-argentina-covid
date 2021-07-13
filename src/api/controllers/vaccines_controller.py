from fastapi import APIRouter
from typing import Optional
from api.services.vaccines_service import get_arrivals, get_bignumbers, get_timeline

router = APIRouter()

# GET ALL VACCINE ARRIVAL DATA
@router.get("/arrivals")
async def list_arrivals():
    arrivals = get_arrivals()
    return arrivals

@router.get("/bignumbers")
async def bignumbers():
    bn = get_bignumbers()
    return bn

@router.get("/timeline")
async def timeline():
    timeline = get_timeline()
    return timeline
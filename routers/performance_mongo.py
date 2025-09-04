from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.performance import PerformanceCreate, PerformanceUpdate, PerformanceOut
from crud import performance_mongo

router = APIRouter(prefix="/performance", tags=["Performance"])

@router.get("/", response_model=List[PerformanceOut])
async def list_performance():
    return await performance_mongo.get_performances()

@router.get("/{performance_id}", response_model=PerformanceOut)
async def get_performance(performance_id: str):
    pf = await performance_mongo.get_performance(performance_id)
    if not pf:
        raise HTTPException(status_code=404, detail="Performance not found")
    return pf

@router.post("/", response_model=PerformanceOut, status_code=status.HTTP_201_CREATED)
async def create_performance(pf: PerformanceCreate):
    return await performance_mongo.create_performance(pf)

@router.put("/{performance_id}", response_model=PerformanceOut)
async def update_performance(performance_id: str, pf: PerformanceUpdate):
    updated = await performance_mongo.update_performance(performance_id, pf)
    if not updated:
        raise HTTPException(status_code=404, detail="Performance not found")
    return updated

@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_performance(performance_id: str):
    deleted = await performance_mongo.delete_performance(performance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Performance not found")
    return None

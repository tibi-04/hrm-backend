from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.performance import PerformanceCreate, PerformanceUpdate, PerformanceOut
from models.performance import Performance
from bson import ObjectId

router = APIRouter(prefix="/performance", tags=["Performance (MongoDB)"])

@router.get("/", response_model=List[PerformanceOut])
async def list_performance():
    performances = Performance.objects.all()
    return [PerformanceOut(**pf.to_mongo().to_dict(), id=str(pf.id)) for pf in performances]

@router.get("/{performance_id}", response_model=PerformanceOut)
async def get_performance(performance_id: str):
    if not ObjectId.is_valid(performance_id):
        raise HTTPException(status_code=400, detail="Invalid performance ID format")
    pf = Performance.objects(id=performance_id).first()
    if not pf:
        raise HTTPException(status_code=404, detail="Performance not found")
    return PerformanceOut(**pf.to_mongo().to_dict(), id=str(pf.id))

@router.post("/", response_model=PerformanceOut, status_code=status.HTTP_201_CREATED)
async def create_performance(performance: PerformanceCreate):
    new_pf = Performance(**performance.dict())
    new_pf.save()
    return PerformanceOut(**new_pf.to_mongo().to_dict(), id=str(new_pf.id))

@router.put("/{performance_id}", response_model=PerformanceOut)
async def update_performance(performance_id: str, performance: PerformanceUpdate):
    if not ObjectId.is_valid(performance_id):
        raise HTTPException(status_code=400, detail="Invalid performance ID format")
    pf = Performance.objects(id=performance_id).first()
    if not pf:
        raise HTTPException(status_code=404, detail="Performance not found")
    pf.update(**performance.dict(exclude_unset=True))
    pf.reload()
    return PerformanceOut(**pf.to_mongo().to_dict(), id=str(pf.id))

@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_performance(performance_id: str):
    if not ObjectId.is_valid(performance_id):
        raise HTTPException(status_code=400, detail="Invalid performance ID format")
    deleted = Performance.objects(id=performance_id).first()
    if not deleted:
        raise HTTPException(status_code=404, detail="Performance not found")
    deleted.delete()
    return None

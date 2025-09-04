from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.leave import LeaveCreate, LeaveUpdate, LeaveOut
from models.leave import Leave
from bson import ObjectId

router = APIRouter(prefix="/leave", tags=["Leave (MongoDB)"])


@router.get("/", response_model=List[LeaveOut])
async def list_leave():
    leaves = Leave.objects.all()
    return [LeaveOut(**leave.to_mongo().to_dict(), id=str(leave.id)) for leave in leaves]


@router.get("/{leave_id}", response_model=LeaveOut)
async def get_leave(leave_id: str):
    if not ObjectId.is_valid(leave_id):
        raise HTTPException(status_code=400, detail="Invalid leave ID format")
    leave = Leave.objects(id=leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return LeaveOut(**leave.to_mongo().to_dict(), id=str(leave.id))


@router.post("/", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
async def create_leave(lv: LeaveCreate):
    leave = Leave(**lv.dict())
    leave.save()
    return LeaveOut(**leave.to_mongo().to_dict(), id=str(leave.id))


@router.put("/{leave_id}", response_model=LeaveOut)
async def update_leave(leave_id: str, lv: LeaveUpdate):
    if not ObjectId.is_valid(leave_id):
        raise HTTPException(status_code=400, detail="Invalid leave ID format")
    leave = Leave.objects(id=leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    leave.update(**{k: v for k, v in lv.dict().items() if v is not None})
    leave.reload()
    return LeaveOut(**leave.to_mongo().to_dict(), id=str(leave.id))


@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leave(leave_id: str):
    if not ObjectId.is_valid(leave_id):
        raise HTTPException(status_code=400, detail="Invalid leave ID format")
    deleted = Leave.objects(id=leave_id).delete()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Leave not found")
    return None

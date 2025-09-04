from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.leave import LeaveCreate, LeaveUpdate, LeaveOut
from crud import leave_mongo

router = APIRouter(prefix="/leave", tags=["Leave"])

@router.get("/", response_model=List[LeaveOut])
async def list_leave():
    return await leave_mongo.get_leaves()

@router.get("/{leave_id}", response_model=LeaveOut)
async def get_leave(leave_id: str):
    lv = await leave_mongo.get_leave(leave_id)
    if not lv:
        raise HTTPException(status_code=404, detail="Leave not found")
    return lv

@router.post("/", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
async def create_leave(lv: LeaveCreate):
    return await leave_mongo.create_leave(lv)

@router.put("/{leave_id}", response_model=LeaveOut)
async def update_leave(leave_id: str, lv: LeaveUpdate):
    updated = await leave_mongo.update_leave(leave_id, lv)
    if not updated:
        raise HTTPException(status_code=404, detail="Leave not found")
    return updated

@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_leave(leave_id: str):
    deleted = await leave_mongo.delete_leave(leave_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Leave not found")
    return None

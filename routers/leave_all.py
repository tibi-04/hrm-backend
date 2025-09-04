# routes/leave_all.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.leave import LeaveOut
from config.mongodb import get_database

router = APIRouter(prefix="/leave_all", tags=["Leave (MongoDB Only)"])

@router.get("/", response_model=List[LeaveOut])
async def list_leave_all(db=Depends(get_database)):
    leaves_cursor = db["leave"].find({})
    leaves = []
    async for leave in leaves_cursor:
        leave["id"] = str(leave["_id"])
        leaves.append(LeaveOut(**leave))
    return leaves

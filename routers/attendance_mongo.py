from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut
from crud import attendance_mongo
from bson import ObjectId

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("/", response_model=List[AttendanceOut], summary="Lấy danh sách chấm công")
async def list_attendance():
    return await attendance_mongo.get_attendances()


@router.get("/{attendance_id}", response_model=AttendanceOut, summary="Xem chi tiết chấm công")
async def get_attendance(attendance_id: str):
    if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    att = await attendance_mongo.get_attendance(attendance_id)
    if not att:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return att


@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED, summary="Tạo bản ghi chấm công")
async def create_attendance(att: AttendanceCreate):
    return await attendance_mongo.create_attendance(att)


@router.put("/{attendance_id}", response_model=AttendanceOut, summary="Cập nhật chấm công")
async def update_attendance(attendance_id: str, att: AttendanceUpdate):
    if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    updated = await attendance_mongo.update_attendance(attendance_id, att)
    if not updated:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return updated


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa bản ghi chấm công")
async def delete_attendance(attendance_id: str):
    if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    deleted = await attendance_mongo.delete_attendance(attendance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return None

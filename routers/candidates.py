from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas.candidate import CandidateCreate, CandidateUpdate, CandidateOut
from crud import candidate_mongo
from datetime import datetime

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.get("/", response_model=List[CandidateOut])
async def list_candidates():
    """Lấy danh sách tất cả ứng viên"""
    try:
        return await candidate_mongo.get_candidates()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách ứng viên: {str(e)}"
        )

@router.post("/", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate: CandidateCreate):
    """Thêm ứng viên mới"""
    try:
        return await candidate_mongo.create_candidate(candidate)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo ứng viên: {str(e)}"
        )

@router.get("/{candidate_id}", response_model=CandidateOut)
async def get_candidate(candidate_id: str):
    """Lấy thông tin ứng viên theo ID"""
    candidate = await candidate_mongo.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy ứng viên"
        )
    return candidate

@router.put("/{candidate_id}", response_model=CandidateOut)
async def update_candidate(candidate_id: str, candidate: CandidateUpdate):
    """Cập nhật thông tin ứng viên"""
    updated = await candidate_mongo.update_candidate(candidate_id, candidate)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy ứng viên"
        )
    return updated

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: str):
    """Xóa ứng viên"""
    deleted = await candidate_mongo.delete_candidate(candidate_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy ứng viên" 
        )
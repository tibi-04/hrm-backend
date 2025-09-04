from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.candidate import CandidateCreate, CandidateUpdate, CandidateOut
from crud import candidate_mongo

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("/filter", response_model=List[CandidateOut])
async def filter_candidates(skill: str = '', min_experience: int = 0):
    return await candidate_mongo.filter_candidates(skill, min_experience)

@router.get("/", response_model=List[CandidateOut])
async def list_candidates():
    return await candidate_mongo.get_candidates()

@router.get("/{candidate_id}", response_model=CandidateOut)
async def get_candidate(candidate_id: str):
    cand = await candidate_mongo.get_candidate(candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return cand

@router.post("/", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
async def create_candidate(cand: CandidateCreate):
    return await candidate_mongo.create_candidate(cand)

@router.put("/{candidate_id}", response_model=CandidateOut)
async def update_candidate(candidate_id: str, cand: CandidateUpdate):
    updated = await candidate_mongo.update_candidate(candidate_id, cand)
    if not updated:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return updated

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: str):
    deleted = await candidate_mongo.delete_candidate(candidate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return None
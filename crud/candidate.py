from sqlalchemy.orm import Session
from models.candidate import Candidate
from schemas.candidate import CandidateCreate, CandidateUpdate
from typing import List, Optional
from fastapi import HTTPException

def skills_to_str(skills):
    return ",".join(skills) if skills else ""

def str_to_skills(skills):
    return [s.strip() for s in skills.split(",") if s.strip()] if skills else []

def get_candidates(db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
    return db.query(Candidate).offset(skip).limit(limit).all() 
def create_candidate(db: Session, cand: CandidateCreate) -> Candidate:

    if db.query(Candidate).filter(Candidate.email == cand.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")
def get_candidate(db: Session, candidate_id: str) -> Optional[Candidate]:
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def create_candidate(db: Session, cand: CandidateCreate) -> Candidate:

    if db.query(Candidate).filter(Candidate.email == cand.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")
    import uuid
    db_cand = Candidate(
        id=str(uuid.uuid4()),
        name=cand.name,
        email=cand.email,
        phone=getattr(cand, 'phone', None),
        address=getattr(cand, 'address', None),
        skills=skills_to_str(cand.skills),
        experience_years=cand.experience_years,
        status=cand.status
    )
    db.add(db_cand)
    db.commit()
    db.refresh(db_cand)
    return db_cand

def update_candidate(db: Session, candidate_id: int, cand: CandidateUpdate) -> Optional[Candidate]:
    db_cand = get_candidate(db, candidate_id)
    if not db_cand:
        return None

    if db.query(Candidate).filter(Candidate.email == cand.email, Candidate.id != candidate_id).first():
        raise HTTPException(status_code=400, detail="Email already exists.")
    db_cand.name = cand.name
    db_cand.email = cand.email
    db_cand.phone = getattr(cand, 'phone', None)
    db_cand.address = getattr(cand, 'address', None)
    db_cand.skills = skills_to_str(cand.skills)
    db_cand.experience_years = cand.experience_years
    db_cand.status = cand.status
    db.commit()
    db.refresh(db_cand)
    return db_cand

def delete_candidate(db: Session, candidate_id: int) -> bool:
    db_cand = get_candidate(db, candidate_id)
    if not db_cand:
        return False
    db.delete(db_cand)
    db.commit()
    return True

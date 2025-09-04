from sqlalchemy.orm import Session
from models.performance import Performance
from schemas.performance import PerformanceCreate, PerformanceUpdate
from typing import List, Optional
from datetime import date

def get_performance(db: Session, performance_id: int) -> Optional[Performance]:
    return db.query(Performance).filter(Performance.id == performance_id).first()

def get_performances(db: Session, skip: int = 0, limit: int = 100) -> List[Performance]:
    return db.query(Performance).offset(skip).limit(limit).all()

def create_performance(db: Session, pf: PerformanceCreate) -> Performance:
    db_pf = Performance(
        employee_id=pf.employee_id,
        review_date=pf.review_date,
        score=pf.score,
        comment=pf.comment
    )
    db.add(db_pf)
    db.commit()
    db.refresh(db_pf)
    return db_pf

def update_performance(db: Session, performance_id: int, pf: PerformanceUpdate) -> Optional[Performance]:
    db_pf = get_performance(db, performance_id)
    if not db_pf:
        return None
    db_pf.employee_id = pf.employee_id
    db_pf.review_date = pf.review_date
    db_pf.score = pf.score
    db_pf.comment = pf.comment
    db.commit()
    db.refresh(db_pf)
    return db_pf

def delete_performance(db: Session, performance_id: int) -> bool:
    db_pf = get_performance(db, performance_id)
    if not db_pf:
        return False
    db.delete(db_pf)
    db.commit()
    return True

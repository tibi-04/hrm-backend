from sqlalchemy.orm import Session
from models.payroll import Payroll
from schemas.payroll import PayrollCreate, PayrollUpdate
from typing import List, Optional
import uuid

def get_payroll(db: Session, payroll_id: str) -> Optional[Payroll]:
    return db.query(Payroll).filter(Payroll.id == payroll_id).first()

def get_payrolls(db: Session, skip: int = 0, limit: int = 100) -> List[Payroll]:
    return db.query(Payroll).offset(skip).limit(limit).all()

def create_payroll(db: Session, pr: PayrollCreate) -> Payroll:
    db_pr = Payroll(
        id=str(uuid.uuid4()),
        employee_id=pr.employee_id,
        month=pr.month,
        base_salary=pr.base_salary,
        bonus=pr.bonus,
        deduction=pr.deduction,
        total=pr.total
    )
    db.add(db_pr)
    db.commit()
    db.refresh(db_pr)
    return db_pr

def update_payroll(db: Session, payroll_id: str, pr: PayrollUpdate) -> Optional[Payroll]:
    db_pr = get_payroll(db, payroll_id)
    if not db_pr:
        return None
    db_pr.employee_id = pr.employee_id
    db_pr.month = pr.month
    db_pr.base_salary = pr.base_salary
    db_pr.bonus = pr.bonus
    db_pr.deduction = pr.deduction
    db_pr.total = pr.total
    db.commit()
    db.refresh(db_pr)
    return db_pr

def delete_payroll(db: Session, payroll_id: int) -> bool:
    db_pr = get_payroll(db, payroll_id)
    if not db_pr:
        return False
    db.delete(db_pr)
    db.commit()
    return True

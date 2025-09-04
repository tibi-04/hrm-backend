from sqlalchemy.orm import Session
from models.department import Department
from schemas.department import DepartmentCreate, DepartmentUpdate
from typing import List, Optional

def get_department(db: Session, department_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
    return db.query(Department).offset(skip).limit(limit).all()

def create_department(db: Session, dep: DepartmentCreate) -> Department:
    db_dep = Department(name=dep.name)
    db.add(db_dep)
    db.commit()
    db.refresh(db_dep)
    return db_dep

def update_department(db: Session, department_id: int, dep: DepartmentUpdate) -> Optional[Department]:
    db_dep = get_department(db, department_id)
    if not db_dep:
        return None
    db_dep.name = dep.name
    db.commit()
    db.refresh(db_dep)
    return db_dep

def delete_department(db: Session, department_id: int) -> bool:
    db_dep = get_department(db, department_id)
    if not db_dep:
        return False
    db.delete(db_dep)
    db.commit()
    return True

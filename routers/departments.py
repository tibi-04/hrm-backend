from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from models.department import Department

router = APIRouter(prefix="/departments", tags=["Departments (MongoDB)"])


@router.get("/", response_model=List[DepartmentOut])
async def list_departments():
    deps = Department.objects.all()
    return [DepartmentOut(**dep.to_mongo().to_dict(), id=str(dep.id)) for dep in deps]


@router.get("/{department_id}", response_model=DepartmentOut)
async def get_department(department_id: str):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")
    dep = Department.objects(id=department_id).first()
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    return DepartmentOut(**dep.to_mongo().to_dict(), id=str(dep.id))


@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
async def create_department(dep: DepartmentCreate):
    new_dep = Department(**dep.dict())
    new_dep.save()
    return DepartmentOut(**new_dep.to_mongo().to_dict(), id=str(new_dep.id))


@router.put("/{department_id}", response_model=DepartmentOut)
async def update_department(department_id: str, dep: DepartmentUpdate):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")
    existing_dep = Department.objects(id=department_id).first()
    if not existing_dep:
        raise HTTPException(status_code=404, detail="Department not found")
    existing_dep.update(**dep.dict(exclude_unset=True))
    updated_dep = Department.objects(id=department_id).first()
    return DepartmentOut(**updated_dep.to_mongo().to_dict(), id=str(updated_dep.id))


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: str):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID")
    deleted = Department.objects(id=department_id).delete()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Department not found")
    return None

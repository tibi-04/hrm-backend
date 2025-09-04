from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from crud import department_mongo
from bson import ObjectId

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=List[DepartmentOut])
async def list_departments():
    return await department_mongo.get_departments()

@router.get("/{department_id}", response_model=DepartmentOut)
async def get_department(department_id: str):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")
    dep = await department_mongo.get_department(department_id)
    if not dep:
        raise HTTPException(status_code=404, detail="Department not found")
    return dep

@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
async def create_department(dep: DepartmentCreate):
    return await department_mongo.create_department(dep)

@router.put("/{department_id}", response_model=DepartmentOut)
async def update_department(department_id: str, dep: DepartmentUpdate):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")
    updated = await department_mongo.update_department(department_id, dep)
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: str):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(status_code=400, detail="Invalid department ID format")
    deleted = await department_mongo.delete_department(department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found")
    return None

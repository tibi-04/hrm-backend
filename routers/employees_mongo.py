from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from crud import employee_mongo
from bson import ObjectId

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/", response_model=List[EmployeeOut])
async def list_employees(department_id: Optional[str] = Query(None, description="Filter by Department ID")):
    employees = await employee_mongo.get_employees()
    if department_id:
        employees = [emp for emp in employees if emp.get("department_id") == department_id]
    return employees

@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(employee_id: str):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    emp = await employee_mongo.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployeeCreate):
    return await employee_mongo.create_employee(emp)

@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee(employee_id: str, emp: EmployeeUpdate):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    updated = await employee_mongo.update_employee(employee_id, emp)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: str):
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID format")
    deleted = await employee_mongo.delete_employee(employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None

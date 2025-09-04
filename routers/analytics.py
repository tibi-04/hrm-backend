from fastapi import APIRouter
from crud.employee_mongo import get_employees
from crud.department_mongo import get_departments

router = APIRouter(prefix="/analytics", tags=["Analytics (MongoDB)"])

@router.get("/employees-by-department")
async def employees_by_department():
    employees = await get_employees()
    departments = await get_departments()

    dept_map = {dep["id"]: dep["name"] for dep in departments}


    department_counts = {}
    for emp in employees:
        dept_id = emp.get("department_id")
        dept_name = dept_map.get(dept_id, "Unknown")
        department_counts[dept_name] = department_counts.get(dept_name, 0) + 1

    return [{"department": dept, "count": count} for dept, count in department_counts.items()]

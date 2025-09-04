from fastapi import APIRouter, Form, HTTPException
from models.user import User
from mongoengine.errors import NotUniqueError
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/admin/create-user")
def create_user_account(
    name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    position: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...) 
):
    if role not in ["employee", "hr", "manager"]:
        raise HTTPException(status_code=400, detail="Role phải là 'employee', 'hr' hoặc 'manager'.")

    try:
        new_user = User(
            email=email,
            hashed_password=bcrypt.hash(password),
            name=name,
            phone=phone,
            address=address,
            position=position,
            avatar="",  
            roles=[role],
            permissions=[],
            is_active=True
        )
        new_user.save()
        return {"message": f"Tạo tài khoản {role} thành công!"}
    except NotUniqueError:
        raise HTTPException(status_code=400, detail="Email đã tồn tại.")

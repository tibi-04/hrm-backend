from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends
from models.user import User
from core.security import get_current_user
from fastapi import APIRouter, HTTPException, Depends, Body
from models.user import User
from core.security import verify_password, get_password_hash, get_current_user

from schemas.user import User as UserSchema
router = APIRouter(prefix="/users", tags=["Users"])
AVATAR_DIR = Path("static/avatars")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)
@router.get("/all", response_model=list[UserSchema])
def get_all_users():
    users = User.objects()
    return [
        UserSchema(
            id=str(u.id),
            email=u.email,
            full_name=u.name or "",
            avatar=u.avatar,
            phone=u.phone,
            address=u.address,
            position=u.position,
            roles=u.roles,
            permissions=u.permissions,
            is_active=u.is_active,
            created_at=str(u.created_at),
            updated_at=str(u.updated_at)
        ) for u in users
    ]

# Xóa tài khoản
@router.delete("/{user_id}")
def delete_user(user_id: str):
    user = User.objects(id=user_id).first()
    if not user:
        return {"msg": "Không tìm thấy tài khoản"}
    user.delete()
    return {"msg": "Đã xóa tài khoản thành công"}

# Sửa thông tin tài khoản
@router.patch("/{user_id}", response_model=UserSchema)
def update_user(user_id: str, data: dict):
    user = User.objects(id=user_id).first()
    if not user:
        return {"msg": "Không tìm thấy tài khoản"}
    # Chỉ cho phép sửa các trường cơ bản
    for field in ["name", "phone", "address", "position", "roles", "permissions", "is_active", "avatar"]:
        if field in data:
            setattr(user, field, data[field])
    user.save()
    return UserSchema(
        id=str(user.id),
        email=user.email,
        full_name=user.name or "",
        avatar=user.avatar,
        phone=user.phone,
        address=user.address,
        position=user.position,
        roles=user.roles,
        permissions=user.permissions,
        is_active=user.is_active,
        created_at=str(user.created_at),
        updated_at=str(user.updated_at)
    )

@router.post("/me/avatar")
async def upload_avatar(
    avatar: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    ext = Path(avatar.filename).suffix or ".png"
    path = AVATAR_DIR / f"{user.id}{ext}"
    with path.open("wb") as f:
        f.write(await avatar.read())

    user.avatar = f"/static/avatars/{user.id}{ext}" 
    user.save()
    return {"url": user.avatar}

@router.put("/me")  
def update_profile(data: dict, user: User = Depends(get_current_user)):
    user.modify(**data)
    return {"msg": "ok"}

@router.post("/me/change-password")
def change_password(
    data: dict = Body(...),
    user: User = Depends(get_current_user),
):
    if not verify_password(data["currentPassword"], user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    new_hashed = get_password_hash(data["newPassword"])
    User.objects(id=user.id).update_one(set__hashed_password=new_hashed)

    return {"msg": "Đổi mật khẩu thành công"}
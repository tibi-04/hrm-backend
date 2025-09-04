
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from models.user import User
from typing import List
from datetime import datetime, timedelta
from core.security import get_current_user

router = APIRouter(prefix="/permission-requests", tags=["Permission Requests"])

class PermissionRequestDeny(BaseModel):
    reason: str

class PermissionRequestCreate(BaseModel):
    function_name: str
    reason: str = ""

class PermissionRequestOut(BaseModel):
    id: str
    manager_id: str
    function_name: str
    status: str
    created_at: str
    expires_at: str

# In-memory store for demo (replace with DB in production)
permission_requests = []

@router.post("/deny/{request_id}")
def deny_permission_request(request_id: str, data: PermissionRequestDeny = Body(...), user: User = Depends(get_current_user)):
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới từ chối yêu cầu quyền.")
    for r in permission_requests:
        if r["id"] == request_id:
            r["status"] = "denied"
            r["deny_reason"] = data.reason
            return {"msg": "Yêu cầu đã bị từ chối.", "reason": data.reason}
    raise HTTPException(status_code=404, detail="Không tìm thấy yêu cầu.")

@router.post("/request", response_model=PermissionRequestOut)
def create_permission_request(data: PermissionRequestCreate, user: User = Depends(get_current_user)):
    if "manager" not in user.roles:
        raise HTTPException(status_code=403, detail="Chỉ manager mới được gửi yêu cầu quyền.")
    now = datetime.utcnow()
    expires = now + timedelta(hours=24)
    req = {
        "id": str(len(permission_requests) + 1),
        "manager_id": str(user.id),
        "function_name": data.function_name,
        "status": "pending",
        "created_at": now.isoformat(),
        "expires_at": expires.isoformat()
    }
    permission_requests.append(req)
    # Gửi thông báo tới admin (giả lập)
    # TODO: Tích hợp notification thực tế
    return req

@router.get("/pending", response_model=List[PermissionRequestOut])
def get_pending_requests(user: User = Depends(get_current_user)):
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới xem được yêu cầu quyền.")
    return [r for r in permission_requests if r["status"] == "pending"]

@router.post("/approve/{request_id}")
def approve_permission_request(request_id: str, user: User = Depends(get_current_user)):
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới duyệt yêu cầu quyền.")
    for r in permission_requests:
        if r["id"] == request_id:
            r["status"] = "approved"
            return {"msg": "Yêu cầu đã được duyệt."}
    raise HTTPException(status_code=404, detail="Không tìm thấy yêu cầu.")

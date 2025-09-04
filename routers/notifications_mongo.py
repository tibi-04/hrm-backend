from fastapi import APIRouter, HTTPException, Depends
from crud.notification_mongo import get_notifications, create_notification, delete_notification, get_active_notifications, update_notification, mark_as_read
from schemas.notification import NotificationCreate, NotificationOut, NotificationUpdate
from typing import List
from routers.auth import get_current_user
from schemas.user import User
from crud.employee_mongo import get_employee_by_email
from bson import ObjectId

router = APIRouter(prefix="/notifications", tags=["notifications"])

async def get_user_department_id(current_user: User) -> str:
    """Lấy department_id từ collection employees dựa trên email"""

    if hasattr(current_user, 'roles') and "admin" in current_user.roles:
        return None
    
    employee = await get_employee_by_email(current_user.email)
    if employee and employee.get("department_id"):
        return str(employee["department_id"])
    return None

@router.get("/", response_model=List[NotificationOut])
async def list_notifications(current_user: User = Depends(get_current_user)):

    user_department_id = await get_user_department_id(current_user)
    
    notifications = await get_notifications()
    

    filtered_notifications = []
    for notification in notifications:

        notification_department_id = notification.get("department_id")
        if (user_department_id is None or 
            not notification_department_id or 
            notification_department_id == user_department_id): 
            filtered_notifications.append(notification)
    
    return filtered_notifications

@router.get("/active", response_model=List[NotificationOut])
async def list_active_notifications(current_user: User = Depends(get_current_user)):
 
    user_department_id = await get_user_department_id(current_user)
    

    notifications = await get_active_notifications() 
    

    filtered_notifications = []
    for notification in notifications:

        notification_department_id = notification.get("department_id")
        if (user_department_id is None or  
            not notification_department_id or  
            notification_department_id == user_department_id):  
            filtered_notifications.append(notification)
    
    return filtered_notifications

@router.post("/", response_model=NotificationOut)
async def add_notification(notification: NotificationCreate, current_user: User = Depends(get_current_user)):

    if not hasattr(current_user, 'roles') or "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền tạo thông báo")
    
    return await create_notification(notification)

@router.patch("/{notification_id}", response_model=NotificationOut)
async def update_notification_endpoint(notification_id: str, notification: NotificationUpdate, current_user: User = Depends(get_current_user)):

    if not hasattr(current_user, 'roles') or "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền cập nhật thông báo")
    
    updated = await update_notification(notification_id, notification.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated

@router.post("/{notification_id}/read", response_model=dict)
async def mark_notification_as_read(notification_id: str, current_user: User = Depends(get_current_user)):
    success = await mark_as_read(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}

@router.delete("/{notification_id}", response_model=dict)
async def remove_notification(notification_id: str, current_user: User = Depends(get_current_user)):

    if not hasattr(current_user, 'roles') or "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền xóa thông báo")
    
    ok = await delete_notification(notification_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}
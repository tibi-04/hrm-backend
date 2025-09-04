from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    content: str
    type: Optional[str] = "general"
    is_active: Optional[bool] = True
    is_read: Optional[bool] = False
    department_id: Optional[str] = None  

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None
    is_read: Optional[bool] = None
    department_id: Optional[str] = None  

class NotificationOut(NotificationBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
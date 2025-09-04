from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RewardBase(BaseModel):
    employee_id: str
    type: str  # reward, punishment, promotion
    reason: Optional[str] = None
    amount: Optional[float] = 0
    date: Optional[datetime] = None

class RewardCreate(RewardBase):
    pass

class RewardUpdate(RewardBase):
    pass

class RewardOut(RewardBase):
    id: str
    class Config:
        from_attributes = True
        

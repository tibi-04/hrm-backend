from models.mongodb import notification_collection
from schemas.notification import NotificationCreate, NotificationUpdate
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

def notification_helper(doc) -> dict:
    department_id = doc.get("department_id")
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "content": doc["content"],
        "created_at": doc.get("created_at", datetime.utcnow().isoformat()),
        "type": doc.get("type", "general"),
        "is_active": doc.get("is_active", True),
        "is_read": doc.get("is_read", False),
        "department_id": str(department_id) if department_id else None 
    }

async def get_notifications() -> List[dict]:
    notifications = []
    async for doc in notification_collection.find().sort("created_at", -1):
        notifications.append(notification_helper(doc))
    return notifications

async def get_active_notifications() -> List[dict]:
    notifications = []
    async for doc in notification_collection.find({"is_active": True}).sort("created_at", -1):
        notifications.append(notification_helper(doc))
    return notifications

async def create_notification(notif: NotificationCreate) -> dict:
    notif_dict = notif.dict()
    notif_dict["created_at"] = datetime.utcnow().isoformat()
    notif_dict["is_active"] = True
    notif_dict["is_read"] = False
    
    if notif_dict.get("department_id") and ObjectId.is_valid(notif_dict["department_id"]):
        notif_dict["department_id"] = ObjectId(notif_dict["department_id"])
    elif notif_dict.get("department_id") == "":
        notif_dict["department_id"] = None
    
    result = await notification_collection.insert_one(notif_dict)
    new_doc = await notification_collection.find_one({"_id": result.inserted_id})
    return notification_helper(new_doc)

async def update_notification(notification_id: str, update_data: dict) -> Optional[dict]:
    if update_data.get("department_id") and ObjectId.is_valid(update_data["department_id"]):
        update_data["department_id"] = ObjectId(update_data["department_id"])
    elif update_data.get("department_id") == "":
        update_data["department_id"] = None
    
    result = await notification_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": update_data}
    )
    if result.modified_count == 1:
        updated_doc = await notification_collection.find_one({"_id": ObjectId(notification_id)})
        return notification_helper(updated_doc)
    return None

async def mark_as_read(notification_id: str) -> bool:
    result = await notification_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"is_read": True}}
    )
    return result.modified_count == 1

async def delete_notification(notification_id: str) -> bool:
    result = await notification_collection.delete_one({"_id": ObjectId(notification_id)})
    return result.deleted_count == 1
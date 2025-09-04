from models.mongodb import user_collection
from schemas.user import UserCreate
from typing import Optional
from bson import ObjectId
import bcrypt

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "full_name": user.get("name", ""),  
        "avatar": user.get("avatar", ""),
        "phone": user.get("phone", ""),
        "address": user.get("address", ""),
        "position": user.get("position", ""),
        "roles": user.get("roles", []),
        "permissions": user.get("permissions", []),
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", "")
    }

async def get_user_by_email(email: str) -> Optional[dict]:
    user = await user_collection.find_one({"email": email})
    return user_helper(user) if user else None

async def create_user(user: UserCreate) -> dict:
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict.pop("password", None)
    

    if "full_name" in user_dict:
        user_dict["name"] = user_dict.pop("full_name")
    
    result = await user_collection.insert_one(user_dict)
    new_user = await user_collection.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

async def get_user_by_id(user_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(user_id):
        return None
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user_helper(user) if user else None
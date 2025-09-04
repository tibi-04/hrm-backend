from models.mongodb import reward_collection
from schemas.reward import RewardCreate, RewardUpdate
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

def reward_helper(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "employee_id": doc["employee_id"],
        "type": doc["type"],
        "reason": doc.get("reason"),
        "amount": doc.get("amount", 0),
        "date": str(doc.get("date")) if doc.get("date") else None,
    }

async def get_rewards() -> List[dict]:
    rewards = []
    async for doc in reward_collection.find():
        rewards.append(reward_helper(doc))
    return rewards

async def create_reward(reward: RewardCreate) -> dict:
    reward_dict = reward.dict()
    if not reward_dict.get("date"):
        reward_dict["date"] = datetime.utcnow().isoformat()
    result = await reward_collection.insert_one(reward_dict)
    new_doc = await reward_collection.find_one({"_id": result.inserted_id})
    return reward_helper(new_doc)

async def delete_reward(reward_id: str) -> bool:
    result = await reward_collection.delete_one({"_id": ObjectId(reward_id)})
    return result.deleted_count == 1

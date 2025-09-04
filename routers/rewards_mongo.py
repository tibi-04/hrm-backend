from fastapi import APIRouter, HTTPException
from crud.reward_mongo import get_rewards, create_reward, delete_reward
from schemas.reward import RewardCreate, RewardOut
from typing import List

router = APIRouter(prefix="/rewards", tags=["rewards"])

@router.get("/", response_model=List[RewardOut])
async def list_rewards():
    return await get_rewards()

@router.post("/", response_model=RewardOut)
async def add_reward(reward: RewardCreate):
    return await create_reward(reward)

@router.delete("/{reward_id}/")
async def remove_reward(reward_id: str):
    ok = await delete_reward(reward_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Reward not found")
    return {"success": True}

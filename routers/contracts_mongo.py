from fastapi import APIRouter, HTTPException
from crud.contract_mongo import get_contracts, create_contract, delete_contract, update_contract as crud_update_contract
from schemas.contract import ContractCreate, ContractOut, ContractUpdate
from typing import List

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.get("/", response_model=List[ContractOut])
async def list_contracts():
    return await get_contracts()

@router.post("/", response_model=ContractOut)
async def add_contract(contract: ContractCreate):
    return await create_contract(contract)

@router.put("/{contract_id}/", response_model=ContractOut)
async def update_contract_endpoint(contract_id: str, contract: ContractUpdate):
    updated_contract = await crud_update_contract(contract_id, contract)
    if not updated_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return updated_contract

@router.delete("/{contract_id}/")
async def remove_contract(contract_id: str):
    ok = await delete_contract(contract_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"success": True}
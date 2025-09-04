from models.mongodb import contract_collection
from schemas.contract import ContractCreate, ContractUpdate
from typing import List, Optional
from bson import ObjectId
from datetime import date

def contract_helper(doc) -> dict:
    return {
        "id": str(doc["_id"]),
        "employee_id": doc["employee_id"],
        "contract_type": doc["contract_type"],
        "start_date": str(doc["start_date"]),
        "end_date": str(doc["end_date"]),
        "status": doc.get("status", "Active"),
        "note": doc.get("note", ""),
        "salary": doc.get("salary", 0),
        "position": doc.get("position", "")
    }

async def get_contracts() -> List[dict]:
    contracts = []
    async for doc in contract_collection.find():
        contracts.append(contract_helper(doc))
    return contracts

async def create_contract(contract: ContractCreate) -> dict:
    contract_dict = contract.dict()
    contract_dict["start_date"] = str(contract_dict["start_date"])
    contract_dict["end_date"] = str(contract_dict["end_date"])
    
    result = await contract_collection.insert_one(contract_dict)
    new_doc = await contract_collection.find_one({"_id": result.inserted_id})
    return contract_helper(new_doc)

async def update_contract(contract_id: str, contract: ContractUpdate) -> Optional[dict]:
    contract_dict = contract.dict(exclude_unset=True)
    
    if 'start_date' in contract_dict:
        contract_dict["start_date"] = str(contract_dict["start_date"])
    if 'end_date' in contract_dict:
        contract_dict["end_date"] = str(contract_dict["end_date"])
    
    result = await contract_collection.update_one(
        {"_id": ObjectId(contract_id)},
        {"$set": contract_dict}
    )
    
    if result.modified_count == 0:
        return None
    
    updated_doc = await contract_collection.find_one({"_id": ObjectId(contract_id)})
    return contract_helper(updated_doc)

async def delete_contract(contract_id: str) -> bool:
    result = await contract_collection.delete_one({"_id": ObjectId(contract_id)})
    return result.deleted_count == 1
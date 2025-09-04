from models.mongodb import candidate_collection, department_collection
from schemas.candidate import CandidateCreate, CandidateUpdate
from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime
import logging

async def filter_candidates(skill: str = '', min_experience: int = 0) -> List[dict]:
    query = {}
    if skill:
        query['skills'] = {'$regex': skill, '$options': 'i'}
    if min_experience > 0:
        query['experience_years'] = {'$gte': min_experience}
    
    candidates = []
    try:
        async for cand in candidate_collection.find(query):
            candidates.append(candidate_helper(cand))
    except Exception as e:
        logging.error(f"[filter_candidates] Lỗi truy vấn MongoDB: {e}")
    return candidates

def candidate_helper(cand) -> dict:
    return {
        "id": str(cand.get("_id", "")),
        "name": cand.get("name", ""),
        "email": cand.get("email", ""),
        "phone": cand.get("phone", None),
        "address": cand.get("address", None),
        "skills": cand.get("skills", []) or [],
        "experience_years": cand.get("experience_years", 0),
        "status": cand.get("status", "Chờ phê duyệt"),
        "position": cand.get("position", None),  
        "department_id": cand.get("department_id", None),  
        "date_of_birth": cand.get("date_of_birth", None),  
        "resume_link": cand.get("resume_link", None),
        "created_at": cand.get("created_at", datetime.now()),
        "updated_at": cand.get("updated_at", datetime.now())
    }

async def get_candidates() -> List[dict]:
    candidates = []
    try:
        async for cand in candidate_collection.find():
            candidate_data = candidate_helper(cand)
            if candidate_data.get("department_id"):
                dept = await department_collection.find_one({"_id": ObjectId(candidate_data["department_id"])})
                if dept:
                    candidate_data["department_name"] = dept.get("name", "")
            candidates.append(candidate_data)
    except Exception as e:
        logging.error(f"[get_candidates] Lỗi truy vấn MongoDB: {e}")
    return candidates

async def get_candidate(candidate_id: str) -> Optional[dict]:
    try:
        cand = await candidate_collection.find_one({"_id": ObjectId(candidate_id)})
        if cand:
            candidate_data = candidate_helper(cand)
            if candidate_data.get("department_id"):
                dept = await department_collection.find_one({"_id": ObjectId(candidate_data["department_id"])})
                if dept:
                    candidate_data["department_name"] = dept.get("name", "")
            return candidate_data
    except Exception as e:
        logging.error(f"[get_candidate] Lỗi truy vấn MongoDB: {e}")
    return None

async def filter_candidates(skill: str = '', min_experience: int = 0) -> List[dict]:
    query = {}
    if skill:
        query['skills'] = {'$regex': skill, '$options': 'i'}
    if min_experience > 0:
        query['experience_years'] = {'$gte': min_experience}
    
    candidates = []
    try:
        async for cand in candidate_collection.find(query):
            candidate_data = candidate_helper(cand)
            if candidate_data.get("department_id"):
                dept = await department_collection.find_one({"_id": ObjectId(candidate_data["department_id"])})
                if dept:
                    candidate_data["department_name"] = dept.get("name", "")
            candidates.append(candidate_data)
    except Exception as e:
        logging.error(f"[filter_candidates] Lỗi truy vấn MongoDB: {e}")
    return candidates

async def get_candidate(candidate_id: str) -> Optional[dict]:
    try:
        cand = await candidate_collection.find_one({"_id": ObjectId(candidate_id)})
        if cand:
            return candidate_helper(cand)
    except Exception as e:
        logging.error(f"[get_candidate] Lỗi truy vấn MongoDB: {e}")
    return None

async def create_candidate(cand: CandidateCreate) -> dict:
    cand_dict = cand.dict()
    
    if isinstance(cand_dict.get("skills"), str):
        cand_dict["skills"] = [s.strip() for s in cand_dict["skills"].split(",") if s.strip()]
    
    cand_dict.setdefault("phone", None)
    cand_dict.setdefault("address", None)
    cand_dict.setdefault("status", "Chờ phê duyệt")
    cand_dict.setdefault("position", None)  
    cand_dict.setdefault("department_id", None)
    cand_dict.setdefault("date_of_birth", None)
    cand_dict.setdefault("resume_link", None)
    cand_dict["created_at"] = datetime.now()
    cand_dict["updated_at"] = datetime.now()
    
    try:
        existing = await candidate_collection.find_one({"email": cand_dict["email"]})
        if existing:
            raise ValueError("Email đã tồn tại trong hệ thống")
            
        result = await candidate_collection.insert_one(cand_dict)
        new_cand = await candidate_collection.find_one({"_id": result.inserted_id})
        return candidate_helper(new_cand)
    except ValueError as ve:
        raise ve
    except Exception as e:
        logging.error(f"[create_candidate] Lỗi tạo ứng viên: {e}")
        raise Exception("Lỗi khi tạo ứng viên")

async def update_candidate(candidate_id: str, cand: CandidateUpdate) -> Optional[dict]:
    update_data = {k: v for k, v in cand.dict(exclude_unset=True).items() if v is not None}
    
    if "skills" in update_data and isinstance(update_data["skills"], str):
        update_data["skills"] = [s.strip() for s in update_data["skills"].split(",") if s.strip()]
    
    if not update_data:
        return None
    
    update_data["updated_at"] = datetime.now()
    
    try:
        await candidate_collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_data}
        )
        updated = await candidate_collection.find_one({"_id": ObjectId(candidate_id)})
        if updated:
            return candidate_helper(updated)
    except Exception as e:
        logging.error(f"[update_candidate] Lỗi cập nhật ứng viên: {e}")
    return None

async def delete_candidate(candidate_id: str) -> bool:
    try:
        result = await candidate_collection.delete_one({"_id": ObjectId(candidate_id)})
        return result.deleted_count == 1
    except Exception as e:
        logging.error(f"[delete_candidate] Lỗi xóa ứng viên: {e}")
        return False
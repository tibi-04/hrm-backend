from fastapi import APIRouter, Query
from typing import List, Optional, Dict, Any
from schemas.candidate import CandidateOut
from crud import candidate_mongo

router = APIRouter(prefix="/candidates-combined", tags=["Candidates Combined"])

@router.get("/", response_model=Dict[str, Any])
async def list_candidates_combined(
    skill: Optional[str] = Query(None),
    min_experience: Optional[int] = Query(0),
    suggest: Optional[bool] = Query(False)
):
    """
    API trả về danh sách ứng viên, cho phép lọc theo kỹ năng và kinh nghiệm, đồng thời trả về gợi ý nếu suggest=True
    """
    candidates = await candidate_mongo.filter_candidates(skill or '', min_experience or 0)

    for c in candidates:
        if '_id' in c:
            del c['_id']
    suggestion = None
    if suggest:
        suggestion = []
        for c in candidates:
            if c.get('experience_years', 0) >= (min_experience or 0):
                suggestion.append({
                    'candidate_id': c['id'],
                    'suggest': 'Nên phỏng vấn',
                    'reason': f"Kinh nghiệm >= {min_experience} năm"
                })
    return {"candidates": candidates, "suggestion": suggestion} 
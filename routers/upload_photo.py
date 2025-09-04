from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/employees/upload-photo")  
async def upload_photo(photo: UploadFile = File(...)):

    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Chỉ cho phép upload file ảnh.")
    save_path = os.path.join(UPLOAD_DIR, photo.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    url = f"/static/avatars/{photo.filename}"
    return JSONResponse({"url": url})

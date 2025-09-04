from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import numpy as np
import cv2
import base64
from datetime import datetime
from pymongo import MongoClient
from io import BytesIO 
from PIL import Image
import face_recognition
import os
from bson import ObjectId
import hashlib
import dlib
from typing import Optional

app = FastAPI()
router = APIRouter()


client = MongoClient(
    "mongodb+srv://dacnktcntt2025:2KBSJeNLEGxDITdn@dacnktcntt.jrfyklb.mongodb.net/DACNKTCNTT?retryWrites=true&w=majority"
)
db = client.DACNKTCNTT

class ImageInput(BaseModel):
    photo_data: str  

class EmployeeUpdate(BaseModel):
    is_deleted: Optional[bool] = None


detector = dlib.get_frontal_face_detector()


current_dir = os.path.dirname(os.path.abspath(__file__))
predictor_path = r"C:\Users\buiha\Downloads\DACN\QLNS\backend\models\shape_predictor_68_face_landmarks.dat"


predictor = dlib.shape_predictor(predictor_path)

def get_image_hash(image_data: bytes) -> str:
    """Generate MD5 hash for image data"""
    return hashlib.md5(image_data).hexdigest()

def convert_to_rgb(image: np.ndarray) -> np.ndarray:
    """Convert image to RGB format properly"""
    try:
        # Check if image has multiple channels
        if len(image.shape) == 2:
            # Grayscale image
            return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif len(image.shape) == 3:
            channels = image.shape[2]
            if channels == 3:
                # Assume BGR format from OpenCV
                return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif channels == 4:
                # RGBA format
                # Convert RGBA to RGB by removing alpha channel
                rgb_image = image[:, :, :3]
                return cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
        
        # If none of the above, return as is
        return image
    except Exception as e:
        print(f"Error converting image to RGB: {str(e)}")
        # Fallback: if conversion fails, try to work with original
        return image

def extract_face_region(image: np.ndarray):
    """Extract face region using facial landmarks"""
    try:
        # Ensure image is in correct format
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Convert RGB to grayscale for dlib
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        elif len(image.shape) == 2:
            # Already grayscale
            gray = image.copy()
        else:
            print(f"Unexpected image shape: {image.shape}")
            return None
        
        # Ensure gray image is uint8
        if gray.dtype != np.uint8:
            gray = gray.astype(np.uint8)
        
        # Detect faces
        faces = detector(gray)
        if len(faces) == 0:
            return None
            
        # Get landmarks for the first face
        landmarks = predictor(gray, faces[0])
        
        # Get coordinates of facial landmarks
        points = np.array([[p.x, p.y] for p in landmarks.parts()])
        min_x, min_y = np.min(points, axis=0)
        max_x, max_y = np.max(points, axis=0)
        
        # Expand the face region slightly (20%)
        width = max_x - min_x
        height = max_y - min_y
        expand_x = int(width * 0.2)
        expand_y = int(height * 0.2)
        
        min_x = max(0, min_x - expand_x)
        min_y = max(0, min_y - expand_y)
        max_x = min(image.shape[1], max_x + expand_x)
        max_y = min(image.shape[0], max_y + expand_y)
        
        # Crop face region from original image
        face_img = image[min_y:max_y, min_x:max_x]
        
        # Resize to standard size for consistent encoding
        face_img = cv2.resize(face_img, (200, 200))
        
        return face_img
    except Exception as e:
        print(f"Error extracting face region: {str(e)}")
        return None

def validate_image_quality(image: np.ndarray) -> bool:
    """Validate image meets quality standards"""
    try:
        # Check image resolution
        if image.shape[0] < 300 or image.shape[1] < 300:
            return False
        
        # Extract face region
        face_img = extract_face_region(image)
        if face_img is None:
            return False
            
        # Check face brightness and contrast
        if len(face_img.shape) == 3:
            gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)
        else:
            gray = face_img
            
        mean_brightness = cv2.mean(gray)[0]
        if mean_brightness < 50 or mean_brightness > 200:
            return False
            
        return True
    except Exception as e:
        print(f"Error validating image quality: {str(e)}")
        return False

def process_face_image(image_data: bytes) -> np.ndarray:
    """Process input image and extract face region"""
    try:
        # Open image using PIL
        img = Image.open(BytesIO(image_data))
        
        # Convert PIL image to numpy array
        img_np = np.array(img)
        
        # Handle different image formats
        if len(img_np.shape) == 2:
            # Grayscale image - convert to RGB
            img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
        elif len(img_np.shape) == 3:
            if img_np.shape[2] == 4:
                # RGBA image - remove alpha channel and convert to RGB
                img_np = img_np[:, :, :3]  # Remove alpha channel
                # PIL loads as RGB, so no need to convert
            elif img_np.shape[2] == 3:
                # RGB image from PIL - already in correct format
                pass
        else:
            raise ValueError(f"Unsupported image format with shape: {img_np.shape}")
        
        # Ensure image is uint8
        if img_np.dtype != np.uint8:
            img_np = img_np.astype(np.uint8)
            
        if not validate_image_quality(img_np):
            raise ValueError("Ảnh không đạt chuẩn chất lượng (cần rõ mặt, đủ sáng)")
            
        # Extract face region
        face_img = extract_face_region(img_np)
        if face_img is None:
            raise ValueError("Không thể xác định khuôn mặt rõ ràng")
            
        return face_img
    except Exception as e:
        raise ValueError(f"Lỗi xử lý ảnh: {str(e)}")

def load_employee_encodings():
    """Load all employee face encodings focusing only on facial features"""
    # Query để lấy tất cả nhân viên chưa bị xóa và có ảnh
    query = {
        "photo_data": {"$exists": True, "$ne": None, "$ne": ""},
        "$or": [
            {"is_deleted": {"$exists": False}},  # Field không tồn tại
            {"is_deleted": False},               # Field = false
            {"is_deleted": None}                 # Field = null
        ]
    }
    
    employees = list(db.employees.find(query))
    encodings = []
    
    # print(f"Found {len(employees)} active employees with photos")
    
    for emp in employees:
        try:
            # Double check - skip if employee is marked as deleted
            if emp.get("is_deleted") is True:
                print(f"Skipping deleted employee: {emp.get('name', 'Unknown')}")
                continue
            
            # Skip if marked as duplicate (if such collection exists)
            if "duplicate_images" in db.list_collection_names():
                if db.duplicate_images.find_one({"image_hash": emp.get("image_hash")}):
                    continue
            
            # Skip if in deleted_employees collection (if exists)
            if "deleted_employees" in db.list_collection_names():
                if db.deleted_employees.find_one({"original_id": emp["_id"]}):
                    continue
            
            # Process photo_data - assuming it's base64 encoded
            photo_data = emp.get("photo_data", "")
            if not photo_data:
                print(f"No photo data for employee: {emp.get('name', 'Unknown')}")
                continue
            
            # Remove data URL prefix if exists (data:image/jpeg;base64,)
            if photo_data.startswith('data:'):
                photo_data = photo_data.split(',')[1]
            
            emp_decoded = base64.b64decode(photo_data)
            face_img = process_face_image(emp_decoded)
            
            if face_img is None:
                # print(f"Could not process face for employee: {emp.get('name', 'Unknown')}")
                continue
            
            # Ensure face image is in RGB format for face_recognition
            if len(face_img.shape) == 3 and face_img.shape[2] == 3:
                rgb_face = face_img  # Already RGB from process_face_image
            else:
                rgb_face = convert_to_rgb(face_img)
            
            # Get encodings from processed face image
            emp_encodings = face_recognition.face_encodings(rgb_face)
            
            if len(emp_encodings) > 0:
                encodings.append({
                    "employee_id": emp["_id"],
                    "name": emp["name"],
                    "email": emp.get("email", ""),
                    "position": emp.get("position", ""),
                    "department_id": emp.get("department_id", ""),
                    "encoding": emp_encodings[0],
                    "image_hash": emp.get("image_hash", "")
                })
                print(f"Successfully loaded encoding for: {emp['name']}")
            else:
                print(f"Could not generate encoding for: {emp.get('name', 'Unknown')}")
                
        except Exception as e:
            print(f"Error processing employee {emp.get('name', 'Unknown')} ({emp.get('_id')}): {str(e)}")
            continue
    
    # print(f"Successfully loaded {len(encodings)} encodings from {len(employees)} employees")
    return encodings

# Initialize encodings
employee_encodings = load_employee_encodings()

def refresh_encodings():
    """Refresh in-memory encodings"""
    global employee_encodings
    employee_encodings = load_employee_encodings()
    return {"status": "success", "count": len(employee_encodings)}

@router.post("/attendance/face")
async def detect_face(data: ImageInput):
    """Endpoint nhận diện khuôn mặt tập trung vào đặc điểm khuôn mặt"""
    try:
        # Refresh encodings mỗi lần gọi để đảm bảo dữ liệu mới nhất
        global employee_encodings
        employee_encodings = load_employee_encodings()
        
        if not employee_encodings:
            return {
                "success": False,
                "detail": "Không có nhân viên nào trong hệ thống hoặc không có ảnh"
            }
        
        # Process input image to get face region
        try:
            # Remove data URL prefix if exists
            photo_data = data.photo_data
            if photo_data.startswith('data:'):
                photo_data = photo_data.split(',')[1]
                
            decoded_data = base64.b64decode(photo_data)
            input_face_img = process_face_image(decoded_data)
            if input_face_img is None:
                raise ValueError("Không thể trích xuất vùng khuôn mặt.")
            
            # Ensure input face image is in RGB format
            if len(input_face_img.shape) == 3 and input_face_img.shape[2] == 3:
                rgb_input = input_face_img  # Already RGB from process_face_image
            else:
                rgb_input = convert_to_rgb(input_face_img)
                
        except Exception as e:
            raise ValueError(f"Dữ liệu ảnh không hợp lệ: {str(e)}")

        # Get encodings from processed face image
        input_encodings = face_recognition.face_encodings(rgb_input)
        if not input_encodings:
            raise ValueError("Không thể trích xuất đặc trưng khuôn mặt")

        # Compare with employee encodings
        best_match = None
        best_distance = 1.0
        all_distances = []  # Track all distances for debugging
        
        # print(f"Comparing with {len(employee_encodings)} employee encodings")
        
        for emp in employee_encodings:
            try:
                # Triple check employee still exists and is not deleted
                employee_exists = db.employees.find_one({
                    "_id": emp["employee_id"],
                    "photo_data": {"$exists": True, "$ne": None, "$ne": ""},
                    "$or": [
                        {"is_deleted": {"$exists": False}},
                        {"is_deleted": False},
                        {"is_deleted": None}
                    ]
                })
                
                if not employee_exists:
                    print(f"Employee {emp['name']} not found or deleted in database")
                    continue
                
                # Check deleted_employees collection if exists
                if "deleted_employees" in db.list_collection_names():
                    if db.deleted_employees.find_one({"original_id": emp["employee_id"]}):
                        print(f"Employee {emp['name']} found in deleted_employees collection")
                        continue
                    
                distance = face_recognition.face_distance([emp["encoding"]], input_encodings[0])[0]
                all_distances.append({
                    "name": emp["name"],
                    "email": emp["email"],
                    "distance": distance
                })
                
                # print(f"Distance to {emp['name']}: {distance:.4f}")
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = emp
                    
            except Exception as e:
                print(f"Error comparing with employee {emp.get('name', 'Unknown')}: {str(e)}")
                continue

        # Stricter threshold - only accept very confident matches
        threshold = 0.4  # Threshold for matching
        
        # print(f"Best match: {best_match['name'] if best_match else 'None'}")
        # print(f"Best distance: {best_distance.item():.4f}")
        # print(f"Threshold: {threshold}")
        formatted_distances = [
    (d["name"], f"{d['distance'].item():.4f}") for d in all_distances[:5]
]
        # print(f"All distances: {formatted_distances}")
        
        if best_match and best_distance < threshold:
            similarity = 1 - best_distance
            
            # Final verification that employee exists and is not deleted
            employee = db.employees.find_one({
                "_id": best_match["employee_id"],
                "$or": [
                    {"is_deleted": {"$exists": False}},
                    {"is_deleted": False},
                    {"is_deleted": None}
                ]
            })
            
            if not employee:
                print(f"Final check failed: Employee {best_match['name']} not found or deleted")
                return {
                    "success": False,
                    "detail": "Không tìm thấy nhân viên phù hợp trong hệ thống"
                }
            
            # Check deleted_employees collection one more time
            if "deleted_employees" in db.list_collection_names():
                if db.deleted_employees.find_one({"original_id": best_match["employee_id"]}):
                    print(f"Final check failed: Employee {best_match['name']} in deleted collection")
                    return {
                        "success": False,
                        "detail": "Không tìm thấy nhân viên phù hợp trong hệ thống"
                    }

            # Create result image with face box
            try:
                full_img = Image.open(BytesIO(decoded_data))
                full_img_np = np.array(full_img)
                
                # Handle different image formats for display
                if len(full_img_np.shape) == 3 and full_img_np.shape[2] == 4:
                    full_img_np = full_img_np[:, :, :3]  # Remove alpha channel
                
                # Convert to RGB for face_recognition
                rgb_full = convert_to_rgb(full_img_np)
                
                # Draw face box on original image
                face_locations = face_recognition.face_locations(rgb_full)
                
                # Convert back to BGR for OpenCV drawing
                display_img = cv2.cvtColor(rgb_full, cv2.COLOR_RGB2BGR)
                
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(display_img, (left, top), (right, bottom), (0, 255, 0), 2)

                # Convert the image with face box to base64
                _, buffer = cv2.imencode('.jpg', display_img)
                image_with_box = base64.b64encode(buffer).decode('utf-8')
            except Exception as e:
                print(f"Error creating result image: {str(e)}")
                image_with_box = None

            # Save attendance record
            attendance_record = {
                "employee_id": best_match["employee_id"],
                "employee_name": best_match["name"],
                "employee_email": best_match["email"],
                "check_in": datetime.now(),
                "method": "face_recognition",
                "confidence": float(similarity),
                "input_image_hash": get_image_hash(decoded_data),
                "created_at": datetime.now()
            }
            
            db.attendance.insert_one(attendance_record)
            # print(f"Attendance recorded for {best_match['name']} with confidence {similarity:.4f}")

            return {
                "success": True,
                "employee": {
                    "id": str(best_match["employee_id"]),
                    "name": best_match["name"],
                    "email": best_match["email"],
                    "position": best_match["position"],
                    "department_id": str(best_match["department_id"]) if best_match["department_id"] else None
                },
                "confidence": float(similarity),
                "image_with_boxes": image_with_box,
                "message": "Nhận diện thành công"
            }
        else:
            # Log failed attempt with more details
            failed_attempt = {
                "timestamp": datetime.now(),
                "input_image_hash": get_image_hash(decoded_data),
                "best_match": str(best_match["employee_id"]) if best_match else None,
                "best_match_name": best_match["name"] if best_match else None,
                "best_distance": float(best_distance) if best_match else None,
                "threshold_used": threshold,
                "all_distances": all_distances,
                "active_employees_count": len(employee_encodings),
                "reason": f"Khoảng cách tốt nhất {best_distance:.4f} > ngưỡng {threshold}"
            }
            
            db.failed_attempts.insert_one(failed_attempt)
            # print(f"Failed recognition attempt logged. Best distance: {best_distance:.4f}")
            
            return {
                "success": False,
                "detail": f"Không tìm thấy nhân viên phù hợp trong hệ thống." if best_match else "Không tìm thấy nhân viên phù hợp trong hệ thống",
                "debug_info": {
                    "best_distance": float(best_distance) if best_match else None,
                    "best_match_name": best_match["name"] if best_match else None,
                    "threshold": threshold,
                    "active_employees": len(employee_encodings),
                    "similarity_percentage": f"{(1-best_distance)*100:.1f}%" if best_match else "0%"
                }
            }

    except Exception as e:
        print(f"Error in detect_face: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Employee management endpoints
@router.put("/employee/{employee_id}/delete")
async def soft_delete_employee(employee_id: str):
    """Soft delete employee by setting is_deleted = true"""
    try:
        obj_id = ObjectId(employee_id)
        
        # Update employee to mark as deleted
        result = db.employees.update_one(
            {"_id": obj_id},
            {
                "$set": {
                    "is_deleted": True,
                    "deleted_at": datetime.now()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Nhân viên không tồn tại")
        
        # Get employee info for backup
        employee = db.employees.find_one({"_id": obj_id})
        if employee:
            # Create backup in deleted_employees if collection doesn't exist
            if "deleted_employees" not in db.list_collection_names():
                db.create_collection("deleted_employees")
                
            # Add to deleted_employees collection for backup
            db.deleted_employees.insert_one({
                "original_id": obj_id,
                "deleted_at": datetime.now(),
                "employee_data": employee
            })
        
        # Refresh encodings immediately
        global employee_encodings
        employee_encodings = load_employee_encodings()
        
        return {
            "success": True,
            "message": f"Đã xóa nhân viên {employee.get('name', 'Unknown')} và cập nhật hệ thống",
            "active_employees": len(employee_encodings),
            "deleted_employee": {
                "id": str(obj_id),
                "name": employee.get("name", "Unknown"),
                "email": employee.get("email", "")
            }
        }
        
    except Exception as e:
        print(f"Error deleting employee: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi xóa nhân viên: {str(e)}")

@router.put("/employee/{employee_id}/restore")
async def restore_employee(employee_id: str):
    """Restore soft deleted employee"""
    try:
        obj_id = ObjectId(employee_id)
        
        # Restore employee by unsetting is_deleted
        result = db.employees.update_one(
            {"_id": obj_id},
            {
                "$unset": {
                    "is_deleted": "",
                    "deleted_at": ""
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Nhân viên không tồn tại")
        
        # Remove from deleted_employees collection
        if "deleted_employees" in db.list_collection_names():
            db.deleted_employees.delete_one({"original_id": obj_id})
        
        # Refresh encodings immediately
        global employee_encodings
        employee_encodings = load_employee_encodings()
        
        employee = db.employees.find_one({"_id": obj_id})
        
        return {
            "success": True,
            "message": f"Đã khôi phục nhân viên {employee.get('name', 'Unknown')} và cập nhật hệ thống",
            "active_employees": len(employee_encodings),
            "restored_employee": {
                "id": str(obj_id),
                "name": employee.get("name", "Unknown"),
                "email": employee.get("email", "")
            }
        }
        
    except Exception as e:
        print(f"Error restoring employee: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khôi phục nhân viên: {str(e)}")

@router.get("/employees/active")
async def get_active_employees():
    """Get list of active employees"""
    try:
        # Get active employees (not soft deleted)
        query = {
            "$or": [
                {"is_deleted": {"$exists": False}},
                {"is_deleted": False},
                {"is_deleted": None}
            ]
        }
        
        employees = list(db.employees.find(
            query,
            {
                "name": 1,
                "email": 1,
                "position": 1,
                "department_id": 1,
                "hire_date": 1,
                "photo_data": 0  # Exclude photo_data for performance
            }
        ))
        
        return {
            "success": True,
            "employees": [
                {
                    "id": str(emp["_id"]),
                    "name": emp["name"],
                    "email": emp.get("email", ""),
                    "position": emp.get("position", ""),
                    "department_id": str(emp["department_id"]) if emp.get("department_id") else None,
                    "hire_date": emp.get("hire_date", "")
                }
                for emp in employees
            ],
            "total": len(employees),
            "encodings_loaded": len(employee_encodings)
        }
    except Exception as e:
        print(f"Error getting active employees: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách nhân viên: {str(e)}")

@router.get("/employees/deleted")
async def get_deleted_employees():
    """Get list of deleted employees"""
    try:
        # Get soft deleted employees
        employees = list(db.employees.find(
            {"is_deleted": True},
            {
                "name": 1,
                "email": 1,
                "position": 1,
                "department_id": 1,
                "deleted_at": 1,
                "photo_data": 0
            }
        ))
        
        return {
            "success": True,
            "deleted_employees": [
                {
                    "id": str(emp["_id"]),
                    "name": emp["name"],
                    "email": emp.get("email", ""),
                    "position": emp.get("position", ""),
                    "department_id": str(emp["department_id"]) if emp.get("department_id") else None,
                    "deleted_at": emp.get("deleted_at", "")
                }
                for emp in employees
            ],
            "total": len(employees)
        }
    except Exception as e:
        print(f"Error getting deleted employees: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi lấy danh sách nhân viên đã xóa: {str(e)}")

@router.post("/refresh-encodings")
async def refresh_encodings_endpoint():
    """Endpoint to manually refresh employee encodings"""
    try:
        result = refresh_encodings()
        return {
            "success": True,
            "message": f"Đã cập nhật {result['count']} encodings",
            **result
        }
    except Exception as e:
        print(f"Error refreshing encodings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error refreshing encodings: {str(e)}")

@router.get("/system/status")
async def get_system_status():
    """Get system status and statistics"""
    try:
        # Count active employees
        active_count = db.employees.count_documents({
            "$or": [
                {"is_deleted": {"$exists": False}},
                {"is_deleted": False},
                {"is_deleted": None}
            ]
        })
        
        # Count deleted employees
        deleted_count = db.employees.count_documents({"is_deleted": True})
        
        # Count employees with photos
        with_photos = db.employees.count_documents({
            "photo_data": {"$exists": True, "$ne": None, "$ne": ""},
            "$or": [
                {"is_deleted": {"$exists": False}},
                {"is_deleted": False},
                {"is_deleted": None}
            ]
        })
        
        # Recent attendance records
        recent_attendance = db.attendance.count_documents({
            "check_in": {"$gte": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)}
        })
        
        return {
            "success": True,
            "system_status": {
                "active_employees": active_count,
                "deleted_employees": deleted_count,
                "employees_with_photos": with_photos,
                "loaded_encodings": len(employee_encodings),
                "today_attendance": recent_attendance,
                "system_time": datetime.now().isoformat()
            }
        }
    except Exception as e:
        print(f"Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi lấy trạng thái hệ thống: {str(e)}")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print(f"Starting server with {len(employee_encodings)} employee encodings loaded")
    uvicorn.run(app, host="0.0.0.0", port=8000)
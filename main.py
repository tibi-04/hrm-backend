from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import mongoengine
import os
from dotenv import load_dotenv
from passlib.hash import bcrypt
from urllib.parse import quote_plus
from models.user import User
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from loguru import logger

from routers import (
    users, auth, employees_mongo, candidates_mongo, departments_mongo,
    attendance_mongo, leave_mongo, payroll_mongo, performance_mongo,
    reports_mongo, notifications_mongo, rewards_mongo, contracts_mongo,
    analytics_mongo, candidates_combined, upload_photo,
    attendance_face, attendance_all, payroll_all, leave_all,users_create,
    permission_requests
)

import bz2
import requests

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat")
MODEL_URL = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"


def download_dlib_model():
    """Tải model dlib nếu chưa có"""
    if not os.path.exists(MODEL_FILE):
        os.makedirs(MODEL_DIR, exist_ok=True)
        compressed_path = MODEL_FILE + ".bz2"
        print("Downloading dlib model... This may take a few minutes.")

        # Tải file .bz2
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(compressed_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("Extracting model...")
        # Giải nén .bz2 -> .dat
        with bz2.BZ2File(compressed_path) as fr, open(MODEL_FILE, "wb") as fw:
            fw.write(fr.read())

        os.remove(compressed_path)
        print("Model downloaded and extracted!")
    else:
        print("Model already exists, skip download.")


load_dotenv()

# Lấy thông tin từ biến môi trường
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB")


MONGODB_URI = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    f"@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority&appName=DACN"
)

try:
    mongoengine.connect(
        db=MONGO_DB,
        host=MONGODB_URI,
        alias="default",
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        serverSelectionTimeoutMS=30000
    )
except Exception:
    pass 


# Khởi tạo Limiter cho rate limiting
limiter = Limiter(key_func=lambda request: request.client.host)

# Khởi tạo FastAPI
app = FastAPI(
    title="HRM System Backend",
    description="Human Resource Management System using MongoDB Atlas",
    version="1.0.0"
)

# Thêm middleware rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Cấu hình loguru để ghi log ra file
logger.add("logs/api_access.log", rotation="10 MB", retention="10 days", level="INFO")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"]
)



# Ghi log cho mọi request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url} từ IP: {request.client.host}")
    response = await call_next(request)
    logger.info(f"Kết thúc {request.method} {request.url} với mã {response.status_code}")
    return response

@app.get("/", tags=["Root"])
@limiter.limit("10/minute")
async def root(request: Request):
    return {
        "message": "HRM Backend is running!"
    }


def init_admin_user():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        return  

    if not User.objects(email=admin_email).first():
        admin = User(
            email=admin_email,
            hashed_password=bcrypt.hash(admin_password),
            name="Admin",
            roles=["admin"],
            permissions=["view_all", "edit_all", "delete_all"],
            is_active=True
        )
        admin.save()


@app.on_event("startup")
async def on_startup():
    try:
        download_dlib_model()   # tải model nếu chưa có
        init_admin_user()
    except Exception as e:
        print("Startup error:", e)


api_routers = [
    users.router, auth.router,
    employees_mongo.router, candidates_mongo.router, departments_mongo.router,
    attendance_mongo.router, leave_mongo.router, payroll_mongo.router,
    performance_mongo.router, reports_mongo.router, notifications_mongo.router,
    rewards_mongo.router, contracts_mongo.router, analytics_mongo.router,
    candidates_combined.router, attendance_face.router,
    attendance_all.router, payroll_all.router, leave_all.router,
    upload_photo.router,users_create.router,
    permission_requests.router
]


# Thêm rate limit cho tất cả các router
for router in api_routers:
    app.include_router(router, prefix="/api")
    router.route_class = limiter.limit("100/minute")


app.mount("/static", StaticFiles(directory="static"), name="static")
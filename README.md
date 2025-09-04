# HRM Backend (FastAPI)

Backend Python cho hệ thống quản lý nhân sự.

## Chức năng chính
- Quản lý nhân sự (employees)
- Quản lý ứng viên (candidates)
- Quản lý phòng ban (departments)
- Chấm công (attendance)
- Tính lương (payroll)
- Nghỉ phép (leave)
- Đánh giá hiệu suất (performance)
- Thống kê – báo cáo (reports)

## Công nghệ sử dụng
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite (hoặc PostgreSQL)

## Khởi động dự án
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

# Hướng dẫn sử dụng Alembic cho migration

## 1. Cài đặt Alembic

```bash
pip install alembic
```

'''
pip install flask flask-cors pymongo bcrypt
'''

## 2. Khởi tạo Alembic

```bash
cd backend
alembic init alembic
```

## 3. Cấu hình Alembic

- Mở file `alembic.ini`, sửa dòng:
  ```ini
  sqlalchemy.url = sqlite:///./hrm.db
  ```
  hoặc nếu dùng PostgreSQL:
  ```ini
  sqlalchemy.url = postgresql://user:password@localhost/dbname
  ```
- Mở file `alembic/env.py`, tìm dòng:
  ```python
  import models
  target_metadata = Base.metadata
  ```
  Đảm bảo đã import đúng models và target_metadata.

## 4. Tạo migration tự động

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## 5. Khi thay đổi models

- Lặp lại bước tạo migration:
  ```bash
  alembic revision --autogenerate -m "update"
  alembic upgrade head
  ```

## 6. Một số lệnh hữu ích

- Xem trạng thái migration:
  ```bash
  alembic current
  ```
- Quay lại migration trước:
  ```bash
  alembic downgrade -1
  ```

---

**Lưu ý:**

- Luôn commit migration vào git để đồng bộ với team.
- Nếu gặp lỗi, kiểm tra lại import models và cấu hình DB URL.

"""
models/__init__.py
Không cần Base.metadata như SQLAlchemy nữa vì dùng MongoEngine.
Chỉ để import các model MongoDB khi cần.
"""

from .user import User
# Nếu cần thêm model MongoDB khác:
# from .employee_mongo import Employee
# from .department_mongo import Department
# ...

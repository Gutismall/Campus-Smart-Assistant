"""
Seed script — inserts mock users into the database.
Run inside the backend container:
  docker exec -it backend python seed.py

Users created:
  admin@campus.com    / password: admin123     (system admin)
  student@campus.com  / password: student123   (student)
  lecturer@campus.com / password: lecturer123  (lecturer)
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://admin:adminpassword@db:5432/campus_data_db"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# Import models AFTER engine is configured
from database import Base
from models.user import User
from models.student import Student
from models.lecturer import Lecturer
from models.campus import Campus
from models.division import Division
from utils.password import hash_password

# ── Create all tables if they don't exist ─────────────────────────────────────
Base.metadata.create_all(bind=engine)

def user_exists(email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None

# ── 1. Admin User ─────────────────────────────────────────────────────────────
if not user_exists("admin@campus.com"):
    admin = User(
        email="admin@campus.com",
        id_number="ADMIN-001",
        hashed_password=hash_password("admin123"),
        is_active=True,
        is_system_admin=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"✅ Admin created   → id={admin.id}  email={admin.email}")
else:
    print("⚠️  Admin already exists, skipping.")

# ── 2. Supporting data: Campus + Division (needed for student & lecturer) ──────
campus = db.query(Campus).filter(Campus.name == "Main Campus").first()
if not campus:
    campus = Campus(name="Main Campus", address_details="1 University Ave")
    db.add(campus)
    db.commit()
    db.refresh(campus)
    print(f"✅ Campus created  → id={campus.id}  name={campus.name}")

division = db.query(Division).filter(Division.name == "Computer Science").first()
if not division:
    division = Division(name="Computer Science", campus_id=campus.id)
    db.add(division)
    db.commit()
    db.refresh(division)
    print(f"✅ Division created → id={division.id}  name={division.name}")

# ── 3. Student User ───────────────────────────────────────────────────────────
if not user_exists("student@campus.com"):
    student_user = User(
        email="student@campus.com",
        id_number="STU-001",
        hashed_password=hash_password("student123"),
        is_active=True,
        is_system_admin=False,
    )
    db.add(student_user)
    db.commit()
    db.refresh(student_user)

    student_profile = Student(
        user_id=student_user.id,
        division_id=division.id,
        enrollment_year=2024,
    )
    db.add(student_profile)
    db.commit()
    print(f"✅ Student created  → user_id={student_user.id}  email={student_user.email}")
else:
    print("⚠️  Student already exists, skipping.")

# ── 4. Lecturer User ──────────────────────────────────────────────────────────
if not user_exists("lecturer@campus.com"):
    lecturer_user = User(
        email="lecturer@campus.com",
        id_number="LEC-001",
        hashed_password=hash_password("lecturer123"),
        is_active=True,
        is_system_admin=False,
    )
    db.add(lecturer_user)
    db.commit()
    db.refresh(lecturer_user)

    lecturer_profile = Lecturer(
        user_id=lecturer_user.id,
        division_id=division.id,
        title="Dr.",
        office_hours="Mon-Wed 10:00-12:00",
    )
    db.add(lecturer_profile)
    db.commit()
    print(f"✅ Lecturer created → user_id={lecturer_user.id}  email={lecturer_user.email}")
else:
    print("⚠️  Lecturer already exists, skipping.")

db.close()
print("\n🎉 Seed complete.")

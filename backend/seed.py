import os
import subprocess
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import engine
from models.user import User
from models.student import Student
from models.lecturer import Lecturer
from models.campus import Campus
from models.division import Division
from utils.password import hash_password

def run_migrations():
    """Runs Alembic upgrade to bring the DB to the latest version."""
    print("📦 Running migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("⚠️  Alembic upgrade stderr:", result.stderr)
    else:
        print("✅ Migrations applied successfully.")

def run_seed():
    """Seeds the DB with basic required data."""
    print("🌱 Running seed data...")
    Session = sessionmaker(bind=engine)
    db = Session()

    def user_exists(email: str) -> bool:
        return db.query(User).filter(User.email == email).first() is not None

    try:
        # 1. Admin
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if not user_exists(admin_email):
            admin = User(
                email=admin_email,
                id_number="ADMIN-001",
                password=hash_password(admin_password),
                is_system_admin=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"✅ Admin created   → id={admin.id} ({admin_email})")
        else:
            print(f"⚙️  Admin {admin_email} already exists.")

        # 2. Campus
        campus = db.query(Campus).filter(Campus.name == "Main Campus").first()
        if not campus:
            campus = Campus(name="Main Campus", address_details="1 University Ave")
            db.add(campus)
            db.commit()
            db.refresh(campus)
            print(f"✅ Campus created  → id={campus.id}")

        # 3. Division
        division = db.query(Division).filter(Division.name == "Computer Science").first()
        if not division:
            division = Division(name="Computer Science", campus_id=campus.id)
            db.add(division)
            db.commit()
            db.refresh(division)
            print(f"✅ Division created → id={division.id}")

        # 4. Student
        if not user_exists("student@campus.com"):
            student_user = User(
                email="student@campus.com",
                id_number="STU-001",
                password=hash_password("student123"),
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
            print(f"✅ Student created  → user_id={student_user.id}")

        # 5. Lecturer
        if not user_exists("lecturer@campus.com"):
            lecturer_user = User(
                email="lecturer@campus.com",
                id_number="LEC-001",
                password=hash_password("lecturer123"),
                is_system_admin=False,
            )
            db.add(lecturer_user)
            db.commit()
            db.refresh(lecturer_user)
            lecturer_profile = Lecturer(
                user_id=lecturer_user.id,
                divisions=[division],
                office_hours=datetime.now(),
            )
            db.add(lecturer_profile)
            db.commit()
            print(f"✅ Lecturer created → user_id={lecturer_user.id}")

        print("🎉 Seed complete.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # When run as a script (CLI/CI), we typically only want to seed data.
    run_seed()

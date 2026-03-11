import os
import subprocess
from datetime import datetime, time, timedelta
from sqlalchemy.orm import sessionmaker
from database import engine
from models import User, Student, Lecturer, Campus, Division, CampusBuilding, Room, Test, StudentTest
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
        # 1. Admin (from .env)
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@campus.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "adminpassword")

        if not user_exists(admin_email):
            admin = User(
                email=admin_email,
                id_number="ADMIN-001",
                password=hash_password(admin_password),
                is_system_admin=True,
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin created   → {admin_email}")
        else:
            print(f"⚙️  Admin {admin_email} already exists.")

        # 2. Campuses
        campuses_data = [
            {"name": "North Campus", "address": "100 North Road"},
            {"name": "South Campus", "address": "200 South Road"}
        ]
        
        db_campuses = []
        for c_data in campuses_data:
            campus = db.query(Campus).filter(Campus.name == c_data["name"]).first()
            if not campus:
                campus = Campus(name=c_data["name"], address_details=c_data["address"])
                db.add(campus)
                db.commit()
                db.refresh(campus)
            db_campuses.append(campus)

        # 3. Divisions (3 per campus)
        divisions_data = {
            "North Campus": ["Computer Science", "Mathematics", "Physics"],
            "South Campus": ["Biology", "Chemistry", "Psychology"]
        }
        
        db_divisions = []
        for campus in db_campuses:
            for div_name in divisions_data[campus.name]:
                div = db.query(Division).filter(Division.name == div_name, Division.campus_id == campus.id).first()
                if not div:
                    div = Division(name=div_name, campus_id=campus.id)
                    db.add(div)
                    db.commit()
                    db.refresh(div)
                db_divisions.append(div)

        # 4. Buildings and Rooms
        db_rooms = []
        building_names = ["Building A", "Building B"]
        for campus in db_campuses:
            for b_name in building_names:
                b_full_name = f"{campus.name} {b_name}"
                building = db.query(CampusBuilding).filter(CampusBuilding.name == b_full_name, CampusBuilding.campus_id == campus.id).first()
                if not building:
                    building = CampusBuilding(campus_id=campus.id, name=b_full_name)
                    db.add(building)
                    db.commit()
                    db.refresh(building)
                
                # Add a few rooms to each building
                for r_num in ["101", "102"]:
                    r_full_number = f"{building.id}-{r_num}"
                    room = db.query(Room).filter(Room.room_number == r_full_number, Room.building_id == building.id).first()
                    if not room:
                        room = Room(
                            building_id=building.id,
                            room_number=r_full_number,
                            capacity=30,
                            available_from=time(8, 0),
                            available_until=time(20, 0)
                        )
                        db.add(room)
                        db.commit()
                        db.refresh(room)
                    db_rooms.append(room)

        # 5. Lecturers
        lecturer_emails = [f"lecturer{i}@campus.com" for i in range(1, 6)]
        for i, email in enumerate(lecturer_emails):
            if not user_exists(email):
                lec_user = User(
                    email=email,
                    id_number=f"LECT-00{i+1}",
                    password=hash_password("lecturer123"),
                    is_system_admin=False
                )
                db.add(lec_user)
                db.commit()
                db.refresh(lec_user)
                
                # Assign to one division (this inherently connects them to a campus)
                div = db_divisions[i % len(db_divisions)]
                lec_profile = Lecturer(
                    user_id=lec_user.id,
                    divisions=[div],
                    office_hours=datetime.now()
                )
                db.add(lec_profile)
                db.commit()
        
        # 6. Students
        student_emails = [f"student{i}@campus.com" for i in range(1, 11)]
        for i, email in enumerate(student_emails):
            if not user_exists(email):
                stu_user = User(
                    email=email,
                    id_number=f"STUD-00{i+1}",
                    password=hash_password("student123"),
                    is_system_admin=False
                )
                db.add(stu_user)
                db.commit()
                db.refresh(stu_user)
                
                # Interleaved divisions (connects student to a campus)
                div = db_divisions[i % len(db_divisions)]
                stu_profile = Student(
                    user_id=stu_user.id,
                    division_id=div.id,
                    enrollment_year=2024
                )
                db.add(stu_profile)
                db.commit()

        # 7. Tests (2 per student)
        all_students = db.query(Student).all()
        for i, student in enumerate(all_students):
            student_campus = student.division.campus
            
            # Find rooms in this student's campus
            campus_rooms = [r for r in db_rooms if r.building.campus_id == student_campus.id]
            
            if not campus_rooms:
                continue
                
            existing_tests = db.query(StudentTest).filter(StudentTest.student_id == student.id).count()
            
            while existing_tests < 2:
                # Assign to a room in their campus
                room = campus_rooms[existing_tests % len(campus_rooms)]
                
                # Create the Test
                test = Test(
                    course_name=f"{student.division.name} Assessment {existing_tests + 1}",
                    date_time=datetime.now() + timedelta(days=5 + existing_tests + i),
                    room_id=room.id
                )
                db.add(test)
                db.commit()
                db.refresh(test)
                
                # Connect student to the test
                student_test = StudentTest(
                    student_id=student.id,
                    test_id=test.id
                )
                db.add(student_test)
                db.commit()
                
                existing_tests += 1

        print("🎉 Seed complete. 1 Admin, 2 Campuses, 6 Divisions, 5 Lecturers, 10 Students with 2 tests each successfully loaded.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()

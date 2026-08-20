# seed.py
from app.database import SessionLocal, engine
from app.models import Base, CourseModel, StudentModel

def seed_database():
    # Ensure tables exist in PostgreSQL
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Clearing old records...")
        db.query(CourseModel).delete()
        db.query(StudentModel).delete()
        db.commit()

        print("Inserting seed data...")
        # Add or modify course records here
        courses = [
            CourseModel(
                title="FastAPI Fundamentals",
                description="Modern REST API development with Python and Pydantic",
                credits=4,
            ),
            CourseModel(
                title="Database Architecture",
                description="Relational database design using PostgreSQL and SQLAlchemy",
                credits=3,
            ),
            CourseModel(
                title="Web Security & Auth",
                description="JWT authentication and rate limiting mechanisms",
                credits=3,
            ),
        ]

        # Add or modify student records here
        students = [
            StudentModel(
                name="Alice Smith",
                email="alice@example.com",
                is_active=True,
            ),
            StudentModel(
                name="Bob Jones",
                email="bob@example.com",
                is_active=True,
            ),
            StudentModel(
                name="Charlie Brown",
                email="charlie@example.com",
                is_active=False,
            ),
        ]

        db.add_all(courses)
        db.add_all(students)
        db.commit()
        print("Database successfully seeded!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
from sqlalchemy import insert, delete
from app.database import engine, metadata
from app.models import courses, students

def seed_database():
    metadata.create_all(bind=engine)
    
    with engine.connect() as conn:
        print("Clearing old records...")
        conn.execute(delete(courses))
        conn.execute(delete(students))
        conn.commit()

        print("Inserting seed data...")
        conn.execute(insert(courses), [
            {
                "title": "FastAPI Fundamentals",
                "description": "Modern REST API development with Python and Pydantic",
                "credits": 4,
            },
            {
                "title": "Database Architecture",
                "description": "Relational database design using PostgreSQL and SQLAlchemy",
                "credits": 3,
            },
        ])

        conn.execute(insert(students), [
            {
                "name": "Alice Smith",
                "email": "alice@example.com",
                "is_active": True,
            },
            {
                "name": "Bob Jones",
                "email": "bob@example.com",
                "is_active": True,
            },
        ])

        conn.commit()
        print("Database successfully seeded using SQLAlchemy Core!")

if __name__ == "__main__":
    seed_database()
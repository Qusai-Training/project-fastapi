from sqlalchemy import Table, Column, Integer, String, Boolean
from app.database import metadata

courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
    Column("credits", Integer, nullable=False),
)

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("is_active", Boolean, default=True),
)
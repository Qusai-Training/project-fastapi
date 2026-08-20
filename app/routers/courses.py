from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, delete
from sqlalchemy.engine import Connection
from app.database import get_db
from app.models import courses
from app.schemas import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseResponse])
def get_courses(title: str | None = None, conn: Connection = Depends(get_db)):
    query = select(courses)
    if title:
        query = query.where(courses.c.title.ilike(f"%{title}%"))
    return conn.execute(query).mappings().all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, conn: Connection = Depends(get_db)):
    query = select(courses).where(courses.c.id == course_id)
    course = conn.execute(query).mappings().first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, conn: Connection = Depends(get_db)):
    stmt = insert(courses).values(**payload.model_dump()).returning(courses)
    new_course = conn.execute(stmt).mappings().first()
    conn.commit()
    return new_course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, conn: Connection = Depends(get_db)):
    query = select(courses).where(courses.c.id == course_id)
    course = conn.execute(query).mappings().first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    stmt = delete(courses).where(courses.c.id == course_id)
    conn.execute(stmt)
    conn.commit()
    return
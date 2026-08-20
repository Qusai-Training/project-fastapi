from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, delete
from sqlalchemy.engine import Connection
from app.database import get_db
from app.models import students
from app.schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(is_active: bool | None = None, conn: Connection = Depends(get_db)):
    query = select(students)
    if is_active is not None:
        query = query.where(students.c.is_active == is_active)
    return conn.execute(query).mappings().all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, conn: Connection = Depends(get_db)):
    query = select(students).where(students.c.id == student_id)
    student = conn.execute(query).mappings().first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, conn: Connection = Depends(get_db)):
    stmt = insert(students).values(**payload.model_dump()).returning(students)
    new_student = conn.execute(stmt).mappings().first()
    conn.commit()
    return new_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, conn: Connection = Depends(get_db)):
    query = select(students).where(students.c.id == student_id)
    student = conn.execute(query).mappings().first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    stmt = delete(students).where(students.c.id == student_id)
    conn.execute(stmt)
    conn.commit()
    return
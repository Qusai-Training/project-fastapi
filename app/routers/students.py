from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Use relative imports (..) to reference files inside the parent app/ folder
from ..database import get_db
from ..models import StudentModel
from ..schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(is_active: bool | None = None, db: Session = Depends(get_db)):
    query = db.query(StudentModel)
    if is_active is not None:
        query = query.filter(StudentModel.is_active == is_active)
    return query.all()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    new_student = StudentModel(**payload.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()
    return
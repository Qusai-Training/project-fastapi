from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Use relative imports (..) to reference files inside the parent app/ folder
from ..database import get_db
from ..models import CourseModel
from ..schemas import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseResponse])
def get_courses(title: str | None = None, db: Session = Depends(get_db)):
    query = db.query(CourseModel)
    if title:
        query = query.filter(CourseModel.title.ilike(f"%{title}%"))
    return query.all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    new_course = CourseModel(**payload.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db.delete(course)
    db.commit()
    return
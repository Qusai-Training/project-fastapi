from pydantic import BaseModel, ConfigDict

# Course Schemas
class CourseBase(BaseModel):
    title: str
    description: str | None = None
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: str
    is_active: bool = True

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
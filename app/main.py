from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import courses, students

app = FastAPI(title="Course Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(students.router)

@app.get("/")
def root():
    return {"status": "Online"}
from fastapi import FastAPI, HTTPException, Query, Path as PathParam, Response
import sqlalchemy as db

from myproject.schemas import Student, Error, StudentUpdate
from myproject.badbd import engine, students, init_db

app = FastAPI(
    title="School API (SQLite)",
    description="Мини-API для списка учеников на SQLite.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.openapi_tags = [
    {"name": "health", "description": "Проверка, что сервер жив"},
    {"name": "students", "desctiption": "Эндпоинты по ученикам"}
]
@app.on_event("startup")
def startup():
    init_db()

@app.get("/", tags=["health"])
def home_page():
    return {"message": "Привет, Мир!"}

@app.get(
    "/students"
)
def get_all_students(
    grade: int | None = Query(None, ge=1, le=11),
    ):
    with engine.begin() as conn:
        stmt = db.select(students).order_by(students.c.student_id)
        if grade is not None:
            stmt = stmt.where(students.c.grade == grade)
        rows = conn.execute(stmt).fetchall()
    return [dict(r._mapping) for r in rows]

@app.get(
    "/students/{grade}"
)
def get_students_by_grade(
    grade: int = PathParam(..., ge=1, le=11),
    last_name: str | None = Query(None),
):
    with engine.begin() as conn:
        stmt = db.select(students).where(students.c.grade == grade)
        if last_name:
            ln = last_name.strip()
            stmt = stmt.where(db.func.lower(students.c.last_name) == db.func.lower(ln))
        
        stmt = stmt.order_by(students.c.student_id)
        rows = conn.execute(stmt).fetchall()
    return [dict(r._mapping) for r in rows]
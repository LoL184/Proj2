from fastapi import FastAPI, HTTPException, Query, Path as PathParam, Response
import sqlalchemy as db
from contextlib import asynccontextmanager

from schemas import Student, Error, StudentUpdate
from badbd import engine, students, init_db


async def lifespan(app: FastAPI):
    init_db()

def create_app() -> FastAPI:

    app = FastAPI(
        title="School API (SQLite)",
        description="Мини-API для списка учеников на SQLite.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
        lifespan=lifespan # pyright: ignore[reportArgumentType]
    )

    app.openapi_tags = [
        {"name": "health", "description": "Проверка, что сервер жив"},
        {"name": "students", "desctiption": "Эндпоинты по ученикам"}
    ]
    
    return app

app = create_app()



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

@app.post("/students",
summary="Создать ученика (POST)",
description="Принимает полную модель Student. Если id уже существует — 409 Conflict.",
status_code=201,
response_model=Student,
responses={
    201: {"description": "Создано"},
    409: {"model": Error, "description": "Ученик с таким ID уже есть"},},
)
def create_student(payload: Student): # payload — это Pydantic-модель Student(валидируется Pydantic)
    with engine.begin() as conn:
        exists = conn.execute(
            db.select(students.c.student_id).where(students.c.student_id == payload.student_id)
        ).fetchall()
        if exists is None:
            raise HTTPException(status_code=409, detail="student_id already exists")
        
        conn.execute(db.insert(students), [payload.model_dump()])

    return payload

@app.put(
        "/students/{student_id}"
)
def replace_student(student_id:int, payload: Student):
    if payload.student_id != student_id:
        raise HTTPException(status_code=400, detail="student_id in path and body must match")
    
    with engine.begin() as conn:
        result = conn.execute(
            db.update(students)
            .where(students.c.student_id == student_id)
            .values(**payload.model_dump(exclude={"student_id"}))
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="student not found")
        
    return payload 


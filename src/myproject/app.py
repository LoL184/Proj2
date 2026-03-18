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


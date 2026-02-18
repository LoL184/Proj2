from fastapi import FastAPI, HTTPException
from myproject.utils import json_to_dict_list
import os
from pathlib import Path
from schemas import Student, Error


DATA = Path(__file__).resolve().parents[1] / "data" / "students.json"

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Мир!"}


@app.get("/students")
def get_all_students():
    try:
        return json_to_dict_list(DATA)
    except FileNotFoundError:
        raise HTTPException(500, "students.json not found")
    
@app.get("/students/{param}")
def get_all_students_grade(param: str):
    if "grade:" in param:
        grade = int(param[param.index('grade:')+6:param.index('grade:')+7:])
        students = json_to_dict_list(DATA)
        return [s for s in students if s.get("grade") == grade]

# @app.get("/students/{param}")
# def get_student_by_id

@app.post("/students",tags=["students"],
summary="Создать ученика (POST)",
description="Принимает полную модель Student. Если student_id уже существует — 409 Conflict.",
status_code=201,
response_model=Student,
responses={
    201: {"description": "Создано"},
    409: {"model": Error, "description": "Ученик с таким ID уже есть"},
    500: {"model": Error, "description": "Файл students.json не найден"}}
)
def create_student(payload: Student): # payload — это Pydantic-модель Student(валидируется Pydantic)
    -code-
        raise HTTPException(status_code=500, detail="students.json not found")
    -code-
        raise HTTPException(status_code=409, detail="student_id already exists")
    # в Pydantic v2 у моделей нет .dict(), вместо этого — .model_dump().
    # метод возвращает обычный словарь Python (готовый к сериализации в JSON).
    # мы добавляем сформированный словарь в список students, т.е. подготавливаем новые данные «в памяти».
    students.append(payload.model_dump())
    DATA.parent.mkdir(parents=True, exist_ok=True)
    dict_list_to_json(students, DATA)
    return payload

def main():
    pass




if __name__ == "__main__":
    main()


# uvicorn myproject.app:app --reload --app-dir src
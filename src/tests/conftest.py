import pytest
import sqlalchemy as db
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
import myproject.bd as db_core
import myproject.app as app_module

@pytest.fixture()
def client():
    # тестовый движок SQLite в памяти (не трогаем students.db)
    test_engine = db.create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Подменяем engine в модулях
    db_core.engine = test_engine
    app_module.engine = test_engine

    # Создаём таблицы
    db_core.metadata.create_all(test_engine)

    # Базовые данные для тестов
    with test_engine.begin() as conn:
        conn.execute(db.delete(db_core.students))
        conn.execute(
            db.insert(db_core.students),
            [
                {
                "student_id": 1,
                "first_name": "Иван",
                "last_name": "Иванов",
                "date_of_birth": "2017-05-15",
                "email": "ivan.ivanov@example.com",
                "phone_number": "+7 (123) 456-7890",
                "address": "Москва",
                "enrollment_year": 2017,
                "grade": 3,
                "special_notes": None,
                },
                {
                "student_id": 2,
                "first_name": "Анна",
                "last_name": "Петрова",
                "date_of_birth": "2016-03-10",
                "email": "anna.petrova@example.com",
                "phone_number": "+7 (999) 111-2233",
                "address": "СПб",
                "enrollment_year": 2016,
                "grade": 3,
                "special_notes": "Перевелась",
                },
                {
                "student_id": 3,
                "first_name": "Илья",
                "last_name": "ИВАНОВ", # для проверки регистронезависимости
                "date_of_birth": "2016-11-20",
                "email": "ilya.ivanov@example.com",
                "phone_number": "+7 (111) 222-3344",
                "address": "Казань",
                "enrollment_year": 2016,
                "grade": 3,
                "special_notes": None,
                },
            ],
        )
    app = app_module.create_app()
    with TestClient(app) as c:
        yield c
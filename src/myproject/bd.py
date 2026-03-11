import sqlalchemy as db

engine = db.create_engine("sqlite:///students.db", future=True)
metadata = db.MetaData()

students = db.Table(
    "students", metadata, 
    db.Column("student_id", db.Integer, primary_key=True),
    db.Column("first_name", db.Text, nullable=False),
    db.Column("last_name", db.Text, nullable=False),
    db.Column("date_of_birth", db.Text, nullable=False), # YYYY-MM-DD
    db.Column("email", db.Text, nullable=False),
    db.Column("phone_number", db.Text, nullable=False),
    db.Column("adress", db.Text, nullable=False),
    db.Column("enrollment_year", db.Integer, nullable=False),
    db.Column("grade", db.Integer, nullable=False),
    db.Column("special_notes", db.Text, nullable=True)
)

metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(
        db.insert(students),
        [
            {
                "student_id": 1,
                "first_name": "Иван",
                "last_name": "Иванов",
                "date_of_birth": "2017-05-15",
                "email": "ivavvan33345@gmail.com",
                "phone_number": "+7 (834) 999-12-49",
                "adress": "г. Нижние Шушары, пр. Ленина, д.1, кв.32",
                "enrollment_year": 2023,
                "grade": 4,
                "special_notes": None
            },
            {
                "student_id": 2,
                "first_name": "ЫВАН",
                "last_name": "ЫВАНОВ",
                "date_of_birth": "1000-13-00",
                "email": "vasvas13@gmail.com",
                "phone_number": "+81 (100) 403-12-49",
                "adress": "г. Угабуга, ул. Военнах приступников, д.2",
                "enrollment_year": 2020,
                "grade": 7,
                "special_notes": None
            }
        ]
    )
    rows = conn.execute(db.select(students).order_by(students.c.student_id)).fetchall()
    print("ALL:", rows)

    print('---------------------------------------')

    rows = conn.execute(
        db.select(students).where(students.c.grade == 4)
    ).fetchall()
    print(rows)

    print('---------------------------------------')

    grade_value = 4
    last_name_value = "иванов"
    rows = conn.execute(
        db.select(students).where(students.c.grade == grade_value).
        where(db.func.lower(students.c.last_name) == db.func.lower(last_name_value)).
        order_by(students.c.student_id)
        ).fetchall()
    print("GRADE 4 + last_name=иванов (case-insensitive):", rows)

    print('---------------------------------------')

    conn.execute(
        db.update(students).where(students.c.student_id == 1).values(grade=4)
    )
    print(conn.execute(db.select(students).order_by(students.c.student_id)).fetchall())

    print('---------------------------------------')

    conn.execute(
        db.delete(students).where(students.c.student_id == 2)
    )
    print(conn.execute(db.select(students).order_by(students.c.student_id)).fetchall())

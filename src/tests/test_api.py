def test_get_students_grade_3(client):
    response = client.get("/students/3")
    assert response.status_code == 200
    data = response.json()
    assert all(s["grade"] == 3 for s in data)

def test_put_replace_ok_and_id_mismatch_400(client):
    # создадим ученика 10
    client.post("/students", json={
        "student_id": 10,
        "first_name": "Пётр",
        "last_name": "Сидоров",
        "date_of_birth": "2016-01-01",
        "email": "petr@example.com",
        "phone_number": "+7 900 000-00-00",
        "address": "Москва",
        "enrollment_year": 2022,
        "grade": 4,
        "special_notes": None,
    })
    ok = {
        "student_id": 10,
        "first_name": "Пётр",
        "last_name": "Сидоров",
        "date_of_birth": "2016-01-01",
        "email": "petr_new@example.com",
        "phone_number": "+7 900 000-00-00",
        "address": "Москва",
        "enrollment_year": 2022,
        "grade": 5,
        "special_notes": "переведён",
    }
    response_ok = client.put("/students/10", json=ok)
    assert response_ok.status_code == 200
    assert response_ok.json()["grade"] == 5
    bad = ok.copy()
    bad["student_id"] = 999
    response_bad = client.put("/students/10", json=bad)
    assert response_bad.status_code == 400

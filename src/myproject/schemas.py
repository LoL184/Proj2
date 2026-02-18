from pydantic import BaseModel, Field

class Student(BaseModel):
    student_id: int = Field(..., description="uniqe student id", ge=1, le=100)
    first_name: str = Field(..., description="Student first name")
    last_name: str = Field(..., description="Student last name")
    date_of_birth: str = Field(..., description="Should contain date like DD-MM-YYYY")
    email: str = Field(..., description="Should contain email")
    phone_number: str = Field(..., description="Should countain phone number like +7 (xxx) xxx-xx-xx")
    address: str = Field(..., description="Should contain real adress")
    enrollment_year: int = Field(..., description="Enrollment year", ge=2020)
    grade: int = Field(..., description="Studying grade", ge=1, le=7)
    special_notes: str | None = Field(..., description="Should be non None if there are notes")


class Error(BaseModel):
    pass
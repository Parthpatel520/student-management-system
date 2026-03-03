from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EnrollmentCreate(BaseModel):
    student_id: UUID
    course_id: UUID
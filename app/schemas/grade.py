from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class GradeCreate(BaseModel):
    enrollment_id: UUID
    marks_obtained: int
    total_marks: int
    remarks: str 
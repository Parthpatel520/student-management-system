from pydantic import BaseModel
from datetime import date

class CreateCouseRequest(BaseModel):
    title: str
    description: str
    credit_hours : int
    max_students : int

class CourseUpdate(BaseModel):
    title: str
    description: str
    credit_hours : int
    max_students : int
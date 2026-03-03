from pydantic import BaseModel
from datetime import date

class StudentRequestAdmin(BaseModel):
    firstname: str
    lastname: str
    phone : str
    date_of_birth : date

class studentPhoneRequest(BaseModel):
    phone: str
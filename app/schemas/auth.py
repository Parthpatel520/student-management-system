from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import date

class Userrole(str, Enum):
    admin = "admin"
    student = "student"
    
class RegisterRequest(BaseModel):
    email : EmailStr
    password : str
    role : Userrole
    firstname : str
    lastname : str
    phone : str
    date_of_birth : date
    
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str
    
class ResendOTPRequest(BaseModel):
    email: EmailStr
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token:str 

from fastapi import APIRouter,Depends,HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.student_profile import Student_ProfileTable
from app.schemas.student import StudentRequestAdmin, studentPhoneRequest



router = APIRouter(prefix="/Student", tags=["Student"])

@router.get("/studentAll")
def Student_all(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    all = db.query(Student_ProfileTable).all()
    
    return all

@router.get("/Find-student/{id}")
def find_student(id:UUID ,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")
    
    id = db.query(Student_ProfileTable).filter(Student_ProfileTable.student_id == id).first()
    
    return id

@router.put("/Update-student/{id}")
def update_student(request: studentPhoneRequest, db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "student" or "admin":
        raise HTTPException(status_code=403, detail="Invalid Role")
    
    phone  = Student_ProfileTable(
        phone = request.phone
    )
    db.add(phone)
    db.commit()
    
    return {"massege": "Phone number Updated"}

@router.put("/Update-student-admin/{id}")
def update_admin(id:UUID, request:StudentRequestAdmin, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    student = db.query(Student_ProfileTable).filter(Student_ProfileTable.user_id == id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    student = Student_ProfileTable(
        firstname = request.firstname,
        lastname = request.lastname,
        phone = request.phone,
        date_of_birth = request.date_of_birth
    )
    
    db.add(student)
    db.commit()
    
    return {"massege": "student Updated successfully"}
    
    
        


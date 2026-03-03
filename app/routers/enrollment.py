from fastapi import APIRouter,Depends,HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.enrollment import EnrollmentTable
from app.schemas.enrollment import EnrollmentCreate



router = APIRouter(prefix="/Enrollment", tags=["Enrollment"])

@router.post("/Create")
def create(request: EnrollmentCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")
    
    existing = db.query(EnrollmentTable).filter(
        EnrollmentTable.student_id == request.student_id,
        EnrollmentTable.course_id == request.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Student already enrolled in this course")

    enrollment = EnrollmentTable(
        student_id=request.student_id,
        course_id=request.course_id
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return {"massege": "New Enrollment Added"}

@router.get("/All")
def all_enrollment(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    all = db.query(EnrollmentTable).all()
    
    return all

@router.get("/GEt-Student-Course/{id}")
def get_student_courses(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "student" or "admin":
        raise HTTPException(status_code=403, detail="Invalid Role")

    enrollments = db.query(EnrollmentTable).filter(
        EnrollmentTable.student_id == id
    ).all()

    return enrollments

@router.get("/GEt-Course-Student/{id}")
def get_course_students(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")

    enrollments = db.query(EnrollmentTable).filter(
        EnrollmentTable.course_id == id
    ).all()

    return enrollments

@router.delete("Delete/{id}")
def delete_enrollment(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")

    enrollment = db.query(EnrollmentTable).filter(
        EnrollmentTable.id == id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()

    return {"message": "Enrollment deleted successfully"}
    
    
        


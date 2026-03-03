from fastapi import APIRouter,Depends,HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.course import CourseTable
from app.schemas.course import CourseUpdate, CreateCouseRequest



router = APIRouter(prefix="/Course", tags=["Course"])

@router.post("/Create")
def create(request: CreateCouseRequest, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    new_course = CourseTable(
        title = request.title,
        description = request.description,
        credit_hours = request.credit_hours,
        max_students = request.max_students
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return{"massege": "New Course Added"}

@router.get("/All")
def course_all(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")
    
    all = db.query(CourseTable).all()
    
    return all

@router.get("/Find-course/{id}")
def find_course(id:UUID ,db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")
    
    course = db.query(CourseTable).filter(CourseTable.course_id == id).first()
    
    return course

@router.put("/Update-Course-admin/{id}")
def update_course(id:UUID, request:CourseUpdate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    course = db.query(CourseTable).filter(CourseTable.course_id == id)
    
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    course = CourseTable(
        title = request.title,
        description = request.description,
        credit_hours = request.credit_hours,
        max_students = request.max_students
        
    )
    
    db.add(course)
    db.commit()
    
    return {"massege": "student Updated successfully"}

@router.delete("Delete/{id}")
def delete_course(id:UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    delete_course = db.query(CourseTable).filter(CourseTable.course_id == id).first()
    
    db.delete(delete_course)
    db.commit()
    db.refresh(delete_course)
    
    return {"massege": "Course Deleted successfully"}
    
    
        


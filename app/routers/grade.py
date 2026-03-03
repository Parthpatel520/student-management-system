from fastapi import APIRouter,Depends,HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.enrollment import EnrollmentTable
from app.models.grade import GradesTable
from app.schemas.grade import GradeCreate
from app.utils.calculate_grade import calculate_grade

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/Create")
def create_grade(request: GradeCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")

    enrollment = db.query(EnrollmentTable).filter(
        EnrollmentTable.id == request.enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    existing = db.query(GradesTable).filter(
        GradesTable.enrollment_id == request.enrollment_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Grade already assigned")

    grade_letter = calculate_grade(request.marks_obtained, request.total_marks)

    grade = GradesTable(
        enrollment_id=request.enrollment_id,
        marks_obtained=request.marks_obtained,
        total_marks=request.total_marks,
        grade_letter=grade_letter,
        remarks=request.remarks
    )

    db.add(grade)
    db.commit()
    db.refresh(grade)

    return grade

@router.get("/All")
def all_grade(db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")
    
    all = db.query(GradesTable).all()
    
    return all

@router.get("/GEt-Grade/{id}")
def get_grade(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")

    grade = db.query(GradesTable).filter(GradesTable.grades_id == id).first()

    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    return grade

@router.put("/Update-Grade/{id}")
def update_grade(id: UUID, data: GradeCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")

    grade = db.query(GradesTable).filter(GradesTable.grades_id == id).first()

    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    grade.marks_obtained = data.marks_obtained
    grade.total_marks = data.total_marks
    grade.grade_letter = calculate_grade(data.marks_obtained, data.total_marks)
    grade.remarks = data.remarks

    db.commit()
    db.refresh(grade)

    return grade

@router.delete("/Delete-Grade/{id}")
def delete_grade(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin Only")

    grade = db.query(GradesTable).filter(GradesTable.grades_id == id).first()

    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    db.delete(grade)
    db.commit()

    return {"message": "Grade deleted successfully"}
    
@router.get("/students/{id}/grades")
def get_student_grades(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")

    grades = db.query(GradesTable).join(EnrollmentTable).filter(
        EnrollmentTable.student_id == id
    ).all()

    return grades   

@router.get("/students/{id}/grades/summary")
def student_summary(id: UUID, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid Role")

    grades = db.query(GradesTable).join(EnrollmentTable).filter(
        EnrollmentTable.student_id == id
    ).all()

    if not grades:
        return {"message": "No grades found"}

    grade_points = {"A":4, "B":3, "C":2, "D":1, "F":0}

    total_points = 0
    total_courses = len(grades)

    for g in grades:
        total_points += grade_points.get(g.grade_letter, 0)

    gpa = total_points / total_courses

    return {
        "total_courses": total_courses,
        "gpa": round(gpa, 2)
    }        


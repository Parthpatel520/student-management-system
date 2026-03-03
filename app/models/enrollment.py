from sqlalchemy import Integer,String,Column,ForeignKey,DateTime,UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class EnrollmentTable(Base):
    __tablename__ = "Enrollment_Table"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True),ForeignKey("Student_Profile_Table.student_id"))
    course_id = Column(UUID(as_uuid=True),ForeignKey("Course_Table.course_id"))
    enrolled_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),
    )
    
    std = relationship("Student_ProfileTable", back_populates="enrols")
    course = relationship("CourseTable", back_populates="enrol")
    grade = relationship("GradesTable", back_populates="enrolg")
    
    






from sqlalchemy import String,Column,DateTime,ForeignKey,Integer
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class GradesTable(Base):
    __tablename__ = "Grades_Table"
    
    grades_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = Column(UUID(as_uuid=True),ForeignKey("Enrollment_Table.id"), nullable=False, unique=True)
    marks_obtained = Column(Integer)
    total_marks = Column(Integer)
    grade_letter = Column(String)
    remarks = Column(String)
    graded_at = Column(DateTime,default=datetime.now)
    
    enrolg = relationship("EnrollmentTable", back_populates="grade", uselist=False)
    
    













from sqlalchemy import Integer,String,Column,DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from sqlalchemy.orm import relationship

class CourseTable(Base):
    __tablename__ = "Course_Table"
    
    course_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    credit_hours = Column(Integer)
    max_students = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
    enrol = relationship("EnrollmentTable",back_populates="course")








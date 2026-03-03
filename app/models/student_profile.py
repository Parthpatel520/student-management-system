from sqlalchemy import String,Column,ForeignKey,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Student_ProfileTable(Base):
    __tablename__ = "Student_Profile_Table"
    
    student_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey("User_Table.user_id"))
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String(12), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    
    User = relationship("UserTable", back_populates="Student_Profile")
    enrols = relationship("EnrollmentTable", back_populates="std")

    
    

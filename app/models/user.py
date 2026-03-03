from sqlalchemy import String,Column,Boolean,DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from sqlalchemy.orm import relationship

class UserTable(Base):
    __tablename__ = "User_Table"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean)
    Created_at = Column(DateTime,default=datetime.now)

    otp_tokens = relationship("OTP_TokenTable", back_populates="user")
    Student_Profile = relationship("Student_ProfileTable", back_populates="User")
    refresh = relationship("Refresh_TokenTable", back_populates="userR")
    
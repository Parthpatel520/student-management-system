from sqlalchemy import Integer,String,Column,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class OTP_TokenTable(Base):
    __tablename__ = "OTP_Token_Table"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey("User_Table.user_id"))
    otp_code = Column(String(6))
    expires_at = Column(DateTime)
    is_used = Column(Boolean)
    
    user = relationship("UserTable", back_populates="otp_tokens")
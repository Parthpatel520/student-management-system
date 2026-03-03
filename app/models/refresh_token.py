from sqlalchemy import String,DateTime,ForeignKey,Column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Refresh_TokenTable(Base):
    __tablename__ = "refresh_tokens"
    
    refresh_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True),ForeignKey("User_Table.user_id"))
    create_at = Column(DateTime, default=datetime.now)
    
    userR = relationship("UserTable", back_populates="refresh")
    
    

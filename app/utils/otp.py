import random
from datetime import datetime,timedelta
from app.config import settings
from app.models.otp_token import OTP_TokenTable
from sqlalchemy.orm import Session
from fastapi import HTTPException,status


def generate_otp():
    """Generate a secure 6-digit OTP"""
    return str(random.randint(100000, 999999))

def create_otp(db:Session, user_id):
    """Generate OTP and save it with expiry"""
    
     # Invalidate previous unused OTPs
    db.query(OTP_TokenTable).filter(
        OTP_TokenTable.user_id == user_id,
        OTP_TokenTable.is_used == False
    ).update({"is_used": True})
    
    otp_code = generate_otp()
    
    expires_at = datetime.now() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    
    otp = OTP_TokenTable(
        user_id=user_id,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False   
    )
    
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp 

def verify_otp(db:Session, user_id, otp_code:str):
    
    otp = (
        db.query(OTP_TokenTable)
        .filter(
            OTP_TokenTable.user_id == user_id,
            OTP_TokenTable.otp_code == otp_code,
            OTP_TokenTable.is_used == False
            )
            .order_by(OTP_TokenTable.created_at.desc())
            .first()
        )
    
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    if otp.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired"
    )

# Mark OTP as used
    otp.is_used = True
    db.commit()

    return True
    



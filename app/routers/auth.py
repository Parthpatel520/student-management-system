from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependencies import get_current_user, get_db
from app.schemas.auth import *

from app.models import *
from app.models.otp_token import OTP_TokenTable

from app.utils.email import send_otp_email
from app.utils.otp import create_otp
from app.utils.hashing import hash_password,verify_password
from app.utils.jwt import create_access_token, create_refreash_token, verify_token,hash_token, create_reset_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(request:RegisterRequest,db:Session = Depends(get_db)):
    
    existing_user = db.query(UserTable).filter(
        UserTable.email == request.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    hashed_password = hash_password(request.password)
    
    new_user = UserTable(
        email = request.email,
        password = hashed_password,
        role = request.role,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_student = Student_ProfileTable(
        firstname = request.firstname,
        lastname = request.lastname,
        phone = request.phone,
        date_of_birth = request.date_of_birth
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    
    otp = create_otp(db , new_user.user_id)
    
    send_otp_email(request.email, otp.otp_code)
    
    return {
        "message": "User registered successfully. Please verify OTP.",
        # "otp_debug": otp.otp_code
    }

@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):

    # Find user
    user = db.query(UserTable).filter(UserTable.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find OTP (latest unused)
    otp_record = (
        db.query(OTP_TokenTable)
        .filter(
            OTP_TokenTable.user_id == user.user_id,
            OTP_TokenTable.is_used == False
        )
        .order_by(OTP_TokenTable.expires_at.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(status_code=400, detail="OTP not found")

    # Check OTP match
    if otp_record.otp_code != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Check expiry
    if otp_record.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="OTP expired")

    # Mark verified
    otp_record.is_used = True
    user.is_verified = True

    db.commit()

    return {"message": "Account verified successfully"}

@router.post("/resend-otp")
async def resend_otp(request: ResendOTPRequest, db: Session = Depends(get_db)):

    # Find user
    user = db.query(UserTable).filter(
        UserTable.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent resend if already verified
    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Account already verified"
        )

    # Create new OTP
    otp = create_otp(db, user.user_id)
    
    send_otp_email(request.email, otp.otp_code)

    return {
        "message": "New OTP sent successfully",
        # "otp_debug": otp.otp_code  # remove in production
    }
    
@router.post("/login")
def login(request: LoginRequest, db:Session = Depends(get_db)):
    
    user = db.query(UserTable).filter(UserTable.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Account not verified")
    
    if user:
        user.is_active = True
    
    access_token = create_access_token(
        data={"sub": str(user.user_id), "role":user.role}
    )
    
    refresh_token = create_refreash_token(
        data={"sub": str(user.user_id), "role":user.role}
    )
    
    hashed_token = hash_token(refresh_token)
    
    db_token = Refresh_TokenTable(
        token = hashed_token,
        user_id = user.user_id
    )
    
    db.add(db_token)
    db.commit()

    
    return{
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"Berer"
    }
    
@router.post("/refreshitoken")
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    
     # Hash incoming token
    hashed = hash_token(request.refresh_token)
    
    db_token = db.query(Refresh_TokenTable).filter(Refresh_TokenTable.token == hashed).first()
    
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh Token")
    
    payload = verify_token(request.refresh_token)
    
    new_access_token = create_access_token(
        data={"sub": str(user.user_id), "role": user.role}
        )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
    
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    
    if current_user.role != "student" or "admin":
        raise HTTPException(status_code=403, detail="Invalid Role")

    hashed = hash_token(refresh_token)

    logout = db.query(Refresh_TokenTable).filter(
        Refresh_TokenTable.token == hashed
    ).delete()
    
    if not logout:
        raise HTTPException("Invalid Token")
    
    if user:
        user.is_active = False

    db.commit()

    return {"message": "Logged out successfully"}
    
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_verified:
        raise HTTPException(status_code=404, detail="User not varified")
    
    otp = create_otp(db, user.user_id)
    
    send_otp_email(email, otp.otp_code)
    
    return {"message": "Password reset OTP sent to your email"}

@router.post("/verify-reset-OTP")
def verify_reset_otp(request:VerifyOTPRequest, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_record = (
        db.query(OTP_TokenTable).filter(
            OTP_TokenTable.user_id == user.user_id,
            OTP_TokenTable.otp_code == request.otp,
            OTP_TokenTable.is_used == False,
        ).first()
    )  
      
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_record.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="OTP expired")
    
    otp_record.is_used = True
    db.commit()
    
    reset_token = create_reset_token(
        data={"sub": str(user.user_id), "type": "password_reset"}
    )

    
    return {
        "reset_token": reset_token,
        "token_type": "bearer"
    }
    
@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):

    payload = verify_token(token)

    if payload.get("type") != "password_reset":
        raise HTTPException(status_code=403, detail="Invalid token type")

    user_id = payload.get("sub")

    user = db.query(UserTable).filter(UserTable.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)

    db.commit()

    return {"message": "Password reset successfully"}
    
    
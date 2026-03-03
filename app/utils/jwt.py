from jose import JWTError,jwt
from app.config import settings
from datetime import datetime, timedelta
import hashlib

def hash_token(token: str) -> str:
    hashed = hashlib.sha256(token.encode())
    return hashed.hexdigest()

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encode_JWT = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encode_JWT

def create_refreash_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    
    encode_JWT = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encode_JWT

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
    
def create_reset_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=settings.CREATE_RESET_TOKEN_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encode_JWT = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encode_JWT

# utils/auth_utils.py

from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from passlib.context import CryptContext
# Set your secret key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password):
    return pwd_context.hash(password)
# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        print("Error creating token:", e)
        return None

# Decode JWT token
def decode_access_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

# ✅ Add this function
def verify_api_key(api_key: str):
    expected_key = os.getenv("API_KEY", "your-default-api-key")
    if api_key == expected_key:
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid API Key")

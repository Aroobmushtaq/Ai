# utils/auth_utils.py

from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from passlib.context import CryptContext
# Set your secret key
SECRET_KEY = "sfgyugb78jkjbhgaujh78yh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
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
#verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        print("Received Token:", token)
        decoded = decode_access_token(token)
        print("Decoded Token:", decoded)
        if decoded is None:
            raise HTTPException(status_code=401, detail="Invalid tokens")
        return decoded
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error verifying token:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
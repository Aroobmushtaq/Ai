from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

# Example static secret key (or use os.getenv("SECRET_KEY"))
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

# Example usage:
if __name__ == "__main__":
    user_data = {"sub": "user@example.com"}  # typically use "sub" (subject) to hold user identifier
    token = create_access_token(user_data)
    print("Generated Token:", token)

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
import os

load_dotenv()
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate(token: str):
    # Dummy token authentication for demonstration
    if not token or token not in os.getenv("USERS"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
import os

load_dotenv()

def authenticate(token: str):
    # Dummy token authentication for demonstration
    
    if token not in str(os.getenv("USERS")).split(","):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
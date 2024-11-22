from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.core.security import SECRET_KEY, ALGORITHM

# OAuth2 scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current user from the JWT token
    Raises HTTPException if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get("sub")
        if phone_number is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    # Get user from database
    user = db.query(User).filter(User.phoneNumber == phone_number).first()
    if user is None:
        raise credentials_exception
        
    return user

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    from app.core.security import create_access_token as security_create_token
    return security_create_token(data)
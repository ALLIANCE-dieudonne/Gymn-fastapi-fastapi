from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schema.schemas import UserCreate, UserLogin, UserResponse
from app.core.security import get_password_hash, verify_password
from app.core.auth import create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Validate phone number length
    if len(user.phoneNumber) != 10:
        raise HTTPException(
            status_code=400,
            detail="Phone number must be 10 characters"
        )
    
    # Check if user exists
    if db.query(User).filter(User.phoneNumber == user.phoneNumber).first():
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        phoneNumber=user.phoneNumber,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.phoneNumber == user_credentials.phoneNumber
    ).first()
    
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.phoneNumber})
    return {"access_token": access_token, "token_type": "bearer"}


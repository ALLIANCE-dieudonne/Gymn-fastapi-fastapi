from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.schema.schemas import UserCreate, UserLogin, UserResponse
from app.core.security import get_password_hash, verify_password
from app.core.auth import create_access_token, get_current_user

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
async def login(
    response: Response,
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with phone number and password
    Returns JWT token if credentials are valid
    """
    # Find user by phone number
    user = db.query(User).filter(
        User.phoneNumber == user_credentials.phoneNumber
    ).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.phoneNumber}
    )
    
    # Set token in cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # for HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "phoneNumber": user.phoneNumber,
            "email": user.email
        }
    }

@router.post("/logout")
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """
    Logout the current user by:
    1. Clearing the access token cookie
    2. Returning a success message
    """
    try:
        # Clear the access token cookie
        response.delete_cookie(
            key="access_token",
            path="/",  # Important: Must match the path used when setting the cookie
            secure=True,  # For HTTPS
            httponly=True,
            samesite="lax"
        )
        
        return {
            "status": "success",
            "message": "Successfully logged out"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {str(e)}"
        )
    
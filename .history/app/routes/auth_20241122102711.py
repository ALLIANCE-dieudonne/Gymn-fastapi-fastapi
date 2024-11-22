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
            status_code=400,from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return self.email


class Enroll(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    gender = models.CharField(max_length=25)
    Dob = models.DateField(auto_now=False, auto_now_add=False)
    membershipPlan = models.CharField(max_length=300)
    trainers = models.CharField(max_length=55)
    reference = models.CharField(max_length=55)
    address = models.TextField()
    paymentStatus = models.CharField(max_length=55, blank=True, null=True)
    price = models.IntegerField(max_length=55, blank=True, null=True)
    dueDate = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.fullname


class Trainer(models.Model):
    name = models.CharField(max_length=55)
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    salary = models.IntegerField(max_length=25)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    plan = models.CharField(max_length=55)
    price = models.IntegerField(max_length=55)

    def __int__(self):
        return self.id

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    img=models.ImageField(upload_to = 'gallery')
    timestamp = models.DateField(auto_now_add=True, blank=True)

    def __int__(self):
        return self.id
    

class Attendance(models.Model):
    phoneNumber = models.CharField(max_length=12)
    selectDate = models.DateField(auto_now_add=True)
    login= models.CharField(max_length=100)
    logout = models.CharField(max_length=100)
    selectWorkout=models.CharField(max_length=100)
    trainedBy=models.CharField(max_length=100)
    
    def __int__(self):
        return self.id
    
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
            path="/", 
            secure=True, 
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
    
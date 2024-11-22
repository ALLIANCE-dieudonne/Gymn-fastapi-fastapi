from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Enroll, User
from app.core.auth import get_current_user
from app.schema.schemas import EnrollResponse

router = APIRouter()

@router.get("/profile", response_model=List[EnrollResponse])
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's profile with their enrollment history
    Requires authentication
    """
    # Get enrollments for the current user
    enrollments = db.query(Enroll).filter(
        Enroll.phoneNumber == current_user.phoneNumber
    ).all()
    
    if not enrollments:
        return []
    
    return enrollments
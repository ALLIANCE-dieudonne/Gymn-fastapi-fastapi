from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Enroll, MembershipPlan, Trainer
from app.schema.schemas import EnrollCreate, EnrollResponse
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/membership-plans")
def get_membership_plans(db: Session = Depends(get_db)):
    return db.query(MembershipPlan).all()

@router.get("/trainers")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@router.post("/enroll", response_model=EnrollResponse)
def create_enrollment(
    enrollment: EnrollCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_enroll = Enroll(**enrollment.dict())
    db.add(db_enroll)
    db.commit()
    db.refresh(db_enroll)
    return db_enroll

@router.get("/profile/enrollments")
def get_user_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    enrollments = db.query(Enroll).filter(
        Enroll.phoneNumber == current_user.phoneNumber
    ).all()
    return enrollments
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Enroll
from app.schema.schemas import EnrollCreate, EnrollResponse
from typing import List

router = APIRouter()

@router.post("/enrollments/", response_model=EnrollResponse)
def create_enrollment(enroll: EnrollCreate, db: Session = Depends(get_db)):
    db_enroll = Enroll(**enroll.dict())
    db.add(db_enroll)
    db.commit()
    db.refresh(db_enroll)
    return db_enroll

@router.get("/enrollments/", response_model=List[EnrollResponse])
def get_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enrollments = db.query(Enroll).offset(skip).limit(limit).all()
    return enrollments

@router.get("/enrollments/{enroll_id}", response_model=EnrollResponse)
def get_enrollment(enroll_id: int, db: Session = Depends(get_db)):
    enrollment = db.query(Enroll).filter(Enroll.id == enroll_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@router.put("/enrollments/{enroll_id}/payment")
def update_payment_status(enroll_id: int, payment_status: str, db: Session = Depends(get_db)):
    enrollment = db.query(Enroll).filter(Enroll.id == enroll_id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.paymentStatus = payment_status
    db.commit()
    return {"message": "Payment status updated"}
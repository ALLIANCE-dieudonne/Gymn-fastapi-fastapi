from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Attendance, Trainer
from app.schema.schemas import AttendanceCreate, AttendanceResponse
from app.core.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/attendance", response_model=AttendanceResponse)
def record_attendance(
    attendance: AttendanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check for existing attendance record
    existing_record = db.query(Attendance).filter(
        Attendance.phoneNumber == attendance.phoneNumber
    ).first()
    
    if existing_record:
        # Update existing record
        for key, value in attendance.dict().items():
            setattr(existing_record, key, value)
        db.commit()
        db.refresh(existing_record)
        return existing_record
    
    # Create new record
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/attendance/trainers")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()
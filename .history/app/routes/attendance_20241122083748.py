from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Attendance
from app.schema.schemas import AttendanceCreate, AttendanceResponse
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/attendance/", response_model=AttendanceResponse)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/attendance/", response_model=List[AttendanceResponse])
def get_attendance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(Attendance).offset(skip).limit(limit).all()
    return records

@router.get("/attendance/date/{date}", response_model=List[AttendanceResponse])
def get_attendance_by_date(date: str, db: Session = Depends(get_db)):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    records = db.query(Attendance).filter(
        Attendance.selectDate >= date_obj,
        Attendance.selectDate < date_obj + timedelta(days=1)
    ).all()
    return records
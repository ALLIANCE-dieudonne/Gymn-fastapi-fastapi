from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Trainer
from app.schema.schemas import TrainerCreate, TrainerResponse
from typing import List

router = APIRouter()

@router.post("/trainers/", response_model=TrainerResponse)
def create_trainer(trainer: TrainerCreate, db: Session = Depends(get_db)):
    db_trainer = Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

@router.get("/trainers/", response_model=List[TrainerResponse])
def get_trainers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trainers = db.query(Trainer).offset(skip).limit(limit).all()
    return trainers

@router.get("/trainers/{trainer_id}", response_model=TrainerResponse)
def get_trainer(trainer_id: int, db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer
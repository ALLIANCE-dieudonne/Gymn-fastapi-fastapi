from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Contact
from app.schema.schemas import ContactCreate, ContactResponse

router = APIRouter()

@router.post("/contact", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(
        name=contact.name,
        email=contact.email,
        phoneNumber=contact.phoneNumber,
        description=contact.description
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
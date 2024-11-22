from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Gallery
from app.schema.schemas import GalleryResponse

router = APIRouter()

@router.get("/gallery", response_model=List[GalleryResponse])
async def get_gallery(db: Session = Depends(get_db)):
    """
    Get all gallery images
    No authentication required
    """
    images = db.query(Gallery).all()
    return images
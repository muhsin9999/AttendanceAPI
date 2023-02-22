from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, utils, oauth2
from app.database import get_db



router = APIRouter(
    prefix="/admins", 
    tags=['Admin']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)
async def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password

    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    db.close()

    return new_admin



@router.get("/all", response_model=List[schemas.AdminOut])
async def get_all_admin(db: Session = Depends(get_db)):

    admin = db.query(models.Admin).all()

    return admin
    



@router.get("/", response_model=schemas.AdminOut)
async def get_admin(
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    admin = db.query(models.Admin).filter(models.Admin.id == current_admin.id).first()
        
    return admin

from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas, utils
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



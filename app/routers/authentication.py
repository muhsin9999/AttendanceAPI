from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(
    admin_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    admin = db.query(models.Admin).filter(
        models.Admin.email == admin_credentials.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials'
        )

    is_password_valid = utils.verify_password(
        admin_credentials.password, admin.password)

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid Credentials'
        )

    access_token = oauth2.create_access_token(data={"admin_id": admin.id})
    return {"access_token": access_token, "token_type": "bearer"}

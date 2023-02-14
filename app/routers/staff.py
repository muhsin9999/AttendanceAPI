from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func



from app import models, schemas, utils, oauth2
from app.database import get_db 


router = APIRouter(
    prefix="/staffs",
    tags=['Staffs'])




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateStaffOut)
async def create_staff(
    staff: schemas.CreateStaff, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    
    new_staff = models.Staff(**staff.dict(), admin_id=current_admin.id)
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    db.close()

    return new_staff



@router.get("/{id}", response_model=schemas.StaffOut)
async def get_staff(
    id: int,
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    
    staff = db.query(
        models.Staff).filter(
            models.Staff.id == id, 
            models.Staff.admin_id == current_admin.id
        ).first()

    if not staff: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with id: {id} not found"
        )
    
    return staff



@router.get("/", response_model=List[schemas.StaffAllOut])
async def get_all_staff(
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    
    all_staff = db.query(
        models.Staff, 
        func.count(models.Image.staff_id).label("image_present_count")
        ).join(
            models.Image, 
            models.Image.staff_id == models.Staff.id, 
            isouter=True
            ).group_by(models.Staff.id
            ).filter(models.Staff.admin_id == current_admin.id
        ).all()

    staffs = []
    for staff, image_count in all_staff:
        staffs.append({
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "gender": staff.gender,
            "phone_number": staff.phone_number,
            "created_at": staff.created_at,
            "admin_id": staff.admin_id,
            "image_present_count": image_count
        })
    
    return staffs



@router.delete("/{id}")
async def delete_staff(
    id: int,  
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    staff = db.query(
        models.Staff).filter(
            models.Staff.id == id, 
            models.Staff.admin_id == current_admin.id
        )

    if staff.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with id: {id} does not exist"
        )
    
    staff.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.CreateStaffOut)
async def update_staff(
    id: int, 
    updated_staff: schemas.CreateStaff, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    staff_query = db.query(
        models.Staff).filter(
            models.Staff.id == id, 
            models.Staff.admin_id == current_admin.id
        )

    staff = staff_query.first()

    if staff == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with id: {id} does not exist"
        )

    staff_query.update(updated_staff.dict(), synchronize_session=False)
    db.commit()

    return staff_query.first()



@router.post("/images/{id}")
async def upload_staff_image(
    id: int,
    file: UploadFile, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    image_data = await file.read()

    if utils.not_image(image_data):
        return {"massage": "invalid image format"}

    staff = db.query( 
        models.Staff).filter(
            models.Staff.id == id,  
            models.Staff.admin_id == current_admin.id
        ).first()

    if not staff: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with id: {id} not found"
        )

    try:
        image = models.Image(
            file_data=image_data, 
            filename=file.filename, 
            staff_id=id, 
        )

        db.add(image)
        db.commit()

        return {"filename": file.filename, "message": "Upload  Successful"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Staff with id: {id} already has a image"
        )
        

    



@router.put("/images/{id}")
async def update_staff_image(
    id: int, 
    file: UploadFile, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    image_data = await file.read()
    if utils.not_image(image_data):
        return {"massage": "invalid image format"}


    staff_image = db.query(
        models.Image).join(
            models.Staff, models.Staff.id == models.Image.staff_id).filter(
                models.Image.staff_id == id, 
                models.Staff.admin_id == current_admin.id
    ).first()

    if not staff_image: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff with id: {id} has no image"
        )

    try:
        staff_image.file_data = image_data
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update profile image"
        )

    finally:
        db.close()

    return {"filename": file.filename, "message": "Update  Successful"}
    


  

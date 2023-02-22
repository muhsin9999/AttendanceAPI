from fastapi import APIRouter, status, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List


from app import schemas, oauth2, database 
from app.routers.repository import staff




router = APIRouter(
    prefix="/staffs",
    tags=['Staffs'])

        
get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateStaffOut)
async def create_staff(
    request: schemas.CreateStaff,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    return staff.create(request, db, current_admin)
    
      


@router.get("/all", response_model=List[schemas.StaffAllOut])
async def show_all_staff(
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    return staff.show_all(db, current_admin)
    



@router.get("/{id}", response_model=schemas.StaffOut)
async def show_staff(
    id: int,
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    
    return staff.show(id, db, current_admin)




@router.delete("/{id}")
async def remove_staff(
    id: int,  
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

   return staff.remove(id, db, current_admin)




@router.put("/{id}", response_model=schemas.CreateStaffOut)
async def update_staff(
    id: int, 
    updated_staff: schemas.CreateStaff, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    return staff.update_st(id, updated_staff, db, current_admin)




@router.post("/images/{id}")
async def upload_staff_image(
    id: int,
    files: List[UploadFile] = File(..., min_items=5, max_items=10),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    await staff.upload(id, files, db, current_admin)

    return {"message": "Upload  Successful"}




@router.post("/capture_images/{id}")
async def capture_staff_image(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    await staff.capture(id, db, current_admin)

    return{"message": "Successful"}




@router.put("/images/{id}")
async def update_staff_image(
    id: int, 
    files: List[UploadFile] = File(..., min_items=5, max_items=10), 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):

    await staff.update_st_image(id, files, db, current_admin)

    return {"message": "Update  Successful"}
    




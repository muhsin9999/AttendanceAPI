from fastapi import APIRouter, status, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional


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
async def get_staff_image(
    id: int,
    action: schemas.StaffImageAction = Query(..., description="Action to perform", example="upload"),
    files: Optional[List[UploadFile]] = File(..., min_items=5, max_items=10),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    if action == schemas.StaffImageAction.upload:
        await staff.upload(id, files, db, current_admin)
        return {"message": "Upload Successful"}
    elif action == schemas.StaffImageAction.capture:
        await staff.capture(id, db, current_admin)
        return {"message": "Capture Successful"}

@router.put("/images/{id}")
async def update_staff_image(
    id: int, 
    files: List[UploadFile] = File(..., min_items=5, max_items=10), 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    await staff.update_st_image(id, files, db, current_admin)
    return {"message": "Update  Successful"}
    




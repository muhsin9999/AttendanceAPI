from fastapi import status, HTTPException, Response
from sqlalchemy import func

from app import models
from app.face_rec import encodings, processimage



def create(staff, db ,current_admin):
    new_staff = models.Staff(**staff.dict(), admin_id=current_admin.id)
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    db.close()
    
    return new_staff



def show_all(db, current_admin):

    all_staff = db.query(
        models.Staff,
        func.count(models.FaceEncoding.staff_id).label("image_present")
        ).join(
            models.FaceEncoding, 
            models.FaceEncoding.staff_id == models.Staff.id, 
            isouter=True
            ).group_by(
                models.Staff.id 
            ).filter(
                models.Staff.admin_id == current_admin.id
    ).all()


    staffs = [{
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "gender": staff.gender,
            "phone_number": staff.phone_number,
            "created_at": staff.created_at,
            "admin_id": staff.admin_id,
            "image_present": image_count
    } for staff, image_count in all_staff]

    return staffs




def show(id, db, current_admin):

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




def remove(id, db, current_admin):

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




def update_st(id, updated_staff, db, current_admin):

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




async def upload(id, files, db, current_admin):

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

    if files is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No item uploaded"
        )

    face_encodings = await processimage.process_image_files(files)

    staff_encoding = models.FaceEncoding(  
        staff_id=id,
        face_encoding=face_encodings
    )

    
    
    try:
        db.add(staff_encoding)
        db.commit()
        db.refresh(staff_encoding)

        db.close()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Staff with id: {id} already has an image"
        )




async def capture(id, db, current_admin):

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
       
    face_encodings = encodings.cam_capture()


    if not face_encodings:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Could not get captures")

    staff_encoding = models.FaceEncoding(  
        staff_id=id,
        face_encoding=face_encodings
    )

    try:
        db.add(staff_encoding)
        db.commit()
        db.refresh(staff_encoding)

        db.close()
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Staff with id: {id} already has an image"
        )

    




async def update_st_image(id, files, db, current_admin):

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

    staff_encoding = db.query(
        models.FaceEncoding).join(
            models.Staff, models.Staff.id == models.FaceEncoding.staff_id).filter(
                models.FaceEncoding.staff_id == id, 
                models.Staff.admin_id == current_admin.id
    ).first()

    if not staff_encoding: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No item to update"
        )

    if files is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No item uploaded"
        )

    face_encodings = await processimage.process_image_files(files)

    row = db.query(models.FaceEncoding).filter(models.FaceEncoding.staff_id == id).first()
    
    
    try:
        row.face_encoding=face_encodings
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update profile image"
        )

    finally:
        db.close()

    
    

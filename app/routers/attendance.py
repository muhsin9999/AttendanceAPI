from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app import models, oauth2
from app.database import get_db
from app.services import attendance_taker


router = APIRouter(
    prefix="/attendance",
    tags=['Attendance'])


@router.post("/{event}/{event_date}")
async def take_attendance(
    event: str,
    event_date: date = Query(date.today().strftime("%Y-%m-%d")),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    today_attendance = attendance_taker.AttendanceTaker(
        db, event, current_admin, event_date)
    response = today_attendance.get_attendance()
    return response


@router.get("/{event}/all")
async def fetch_all_attendance(
    event: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    existing_record_query = db.query(models.Attendance).filter(
        models.Attendance.admin_id == current_admin.id,
        models.Attendance.event == event.capitalize()
    )
    existing_record = existing_record_query.first()
    if not existing_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Record found"
        )
    existing_records = existing_record_query
    event_dates = [record.event_date for record in existing_records]
    unique_dates = list(set(event_dates))

    record = attendance_taker.AttendanceTaker(db, event, current_admin)
    response = record.response(unique_dates)
    return response


@router.get("/{event}/{event_date}")
async def fetch_attendance(
    event: str,
    event_date: date = Query(date.today().strftime("%Y-%m-%d")),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    existing_record = db.query(models.Attendance).filter(
        models.Attendance.admin_id == current_admin.id,
        models.Attendance.event_date == event_date,
        models.Attendance.event == event.capitalize()
    ).first()
    if not existing_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Record found"
        )
    record = attendance_taker.AttendanceTaker(
        db, event, current_admin, event_date)
    response = record.response()
    return response


@router.delete("/{event}/{event_date}")
async def delete_attendance(
    event: str,
    event_date: date = Query(date.today().strftime("%Y-%m-%d")),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(oauth2.get_current_admin)
):
    record = attendance_taker.AttendanceTaker(
        db, event, current_admin, event_date)
    response = record.delete_attendance()
    return response
